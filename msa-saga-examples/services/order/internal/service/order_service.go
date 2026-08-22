package service

import (
	"context"
	"database/sql"
	"encoding/json"
	stderrors "errors"
	"fmt"
	"time"

	"github.com/google/uuid"
	"github.com/kyungseok/msa-saga-go-examples/common/errors"
	"github.com/kyungseok/msa-saga-go-examples/common/events"
	"github.com/kyungseok/msa-saga-go-examples/services/order/internal/domain"
	"github.com/kyungseok/msa-saga-go-examples/services/order/internal/repository"
	"go.uber.org/zap"
)

// CreateOrderCommand 주문 생성 커맨드
type CreateOrderCommand struct {
	UserID         int64
	Amount         int64
	Quantity       int
	IdempotencyKey string
}

// CreateOrderResult 주문 생성 결과
type CreateOrderResult struct {
	OrderID int64
	Status  domain.OrderStatus
}

// OrderService 주문 서비스 인터페이스
type OrderService interface {
	CreateOrder(ctx context.Context, cmd CreateOrderCommand) (*CreateOrderResult, error)
	GetOrder(ctx context.Context, orderID int64) (*domain.Order, error)
	HandlePaymentCompleted(ctx context.Context, evt events.PaymentCompletedEvent) error
	HandlePaymentFailed(ctx context.Context, evt events.PaymentFailedEvent) error
	HandleStockReserved(ctx context.Context, evt events.StockReservedEvent) error
	HandleStockReservationFailed(ctx context.Context, evt events.StockReservationFailedEvent) error
	HandleDeliveryStarted(ctx context.Context, evt events.DeliveryStartedEvent) error
	HandleDeliveryFailed(ctx context.Context, evt events.DeliveryFailedEvent) error
}

type orderService struct {
	db         *sql.DB
	orderRepo  repository.OrderRepository
	outboxRepo repository.OutboxRepository
	logger     *zap.Logger
}

// NewOrderService 주문 서비스 생성
func NewOrderService(
	db *sql.DB,
	orderRepo repository.OrderRepository,
	outboxRepo repository.OutboxRepository,
	logger *zap.Logger,
) OrderService {
	return &orderService{
		db:         db,
		orderRepo:  orderRepo,
		outboxRepo: outboxRepo,
		logger:     logger,
	}
}

// CreateOrder 주문 생성 (Outbox 패턴 적용)
func (s *orderService) CreateOrder(ctx context.Context, cmd CreateOrderCommand) (*CreateOrderResult, error) {
	// 멱등성 체크 (조회 실패는 fail-closed: ErrNoRows일 때만 신규 진행)
	if cmd.IdempotencyKey != "" {
		existing, err := s.orderRepo.FindByIdempotencyKey(ctx, cmd.IdempotencyKey)
		if err == nil {
			s.logger.Info("order already exists with idempotency key",
				zap.String("idempotencyKey", cmd.IdempotencyKey),
				zap.Int64("orderId", existing.ID))
			return &CreateOrderResult{
				OrderID: existing.ID,
				Status:  existing.Status,
			}, nil
		}
		if !stderrors.Is(err, sql.ErrNoRows) {
			return nil, errors.Wrap(errors.ErrCodeDatabaseError, "failed to check idempotency key", err)
		}
	}

	// 입력 검증
	if cmd.Amount <= 0 {
		return nil, errors.New(errors.ErrCodeInvalidOrder, "amount must be positive")
	}
	if cmd.Quantity <= 0 {
		return nil, errors.New(errors.ErrCodeInvalidOrder, "quantity must be positive")
	}

	// 트랜잭션 시작
	tx, err := s.db.BeginTx(ctx, nil)
	if err != nil {
		return nil, errors.Wrap(errors.ErrCodeDatabaseError, "failed to begin transaction", err)
	}
	defer tx.Rollback()

	// 주문 생성
	now := time.Now()
	order := &domain.Order{
		UserID:         cmd.UserID,
		Amount:         cmd.Amount,
		Quantity:       cmd.Quantity,
		Status:         domain.OrderStatusPending,
		IdempotencyKey: cmd.IdempotencyKey,
		CreatedAt:      now,
		UpdatedAt:      now,
	}

	if err := s.orderRepo.CreateTx(ctx, tx, order); err != nil {
		return nil, errors.Wrap(errors.ErrCodeDatabaseError, "failed to create order", err)
	}

	// SAGA 시작: OrderCreated 이벤트 생성
	correlationID := uuid.New().String()
	event := events.OrderCreatedEvent{
		BaseEvent: events.BaseEvent{
			EventID:       uuid.New().String(),
			EventType:     events.EventOrderCreated,
			SchemaVersion: 1,
			OccurredAt:    now,
			CorrelationID: correlationID,
		},
		OrderID:  order.ID,
		UserID:   order.UserID,
		Amount:   order.Amount,
		Quantity: order.Quantity,
	}

	payload, err := json.Marshal(event)
	if err != nil {
		return nil, errors.Wrap(errors.ErrCodeSerializationError, "failed to marshal event", err)
	}

	// Outbox에 이벤트 저장 (트랜잭션과 함께 커밋)
	outboxEvent := &repository.OutboxEvent{
		AggregateType: "order",
		AggregateID:   order.ID,
		EventType:     string(events.EventOrderCreated),
		Payload:       payload,
		Status:        "PENDING",
		CreatedAt:     now,
	}

	if err := s.outboxRepo.InsertTx(ctx, tx, outboxEvent); err != nil {
		return nil, errors.Wrap(errors.ErrCodeDatabaseError, "failed to insert outbox event", err)
	}

	// 트랜잭션 커밋
	if err := tx.Commit(); err != nil {
		return nil, errors.Wrap(errors.ErrCodeDatabaseError, "failed to commit transaction", err)
	}

	s.logger.Info("order created successfully",
		zap.Int64("orderId", order.ID),
		zap.String("correlationId", correlationID))

	return &CreateOrderResult{
		OrderID: order.ID,
		Status:  order.Status,
	}, nil
}

// GetOrder 주문 조회
func (s *orderService) GetOrder(ctx context.Context, orderID int64) (*domain.Order, error) {
	order, err := s.orderRepo.FindByID(ctx, orderID)
	if err != nil {
		if stderrors.Is(err, sql.ErrNoRows) {
			return nil, errors.New(errors.ErrCodeOrderNotFound, fmt.Sprintf("order not found: %d", orderID))
		}
		return nil, errors.Wrap(errors.ErrCodeDatabaseError, "failed to find order", err)
	}
	return order, nil
}

// transition 주문 상태 전이 공통 헬퍼.
//   - 도메인 전이 규칙(CanTransitionTo) 위반은 에러가 아니라 경고 로그 후 무시 (이미 처리됐거나 지나간 상태의 이벤트 재수신 시나리오)
//   - Optimistic Lock 버전 충돌도 에러가 아니라 경고 로그 후 무시 (다른 핸들러가 먼저 처리한 경우. 재전달되지 않음)
func (s *orderService) transition(ctx context.Context, o *domain.Order, next domain.OrderStatus) error {
	if !o.CanTransitionTo(next) {
		s.logger.Warn("illegal status transition ignored",
			zap.Int64("orderId", o.ID),
			zap.String("current", string(o.Status)),
			zap.String("next", string(next)))
		return nil
	}

	updated, err := s.orderRepo.UpdateStatusWithVersion(ctx, o.ID, next, o.Version)
	if err != nil {
		return fmt.Errorf("failed to update order status: %w", err)
	}
	if !updated {
		s.logger.Warn("version conflict during status transition, skipping",
			zap.Int64("orderId", o.ID),
			zap.String("current", string(o.Status)),
			zap.String("next", string(next)),
			zap.Int64("version", o.Version))
		return nil
	}

	o.Status = next
	o.Version++
	s.logger.Info("order status updated",
		zap.Int64("orderId", o.ID),
		zap.String("status", string(next)))
	return nil
}

// findByOrderID 이벤트 핸들러용 주문 조회 (미존재만 비즈니스 에러로 변환)
func (s *orderService) findByOrderID(ctx context.Context, orderID int64, eventType string) (*domain.Order, error) {
	order, err := s.orderRepo.FindByID(ctx, orderID)
	if err != nil {
		if stderrors.Is(err, sql.ErrNoRows) {
			return nil, errors.New(errors.ErrCodeOrderNotFound, fmt.Sprintf("%s: order not found: %d", eventType, orderID))
		}
		return nil, fmt.Errorf("%s: failed to find order: %w", eventType, err)
	}
	return order, nil
}

// HandlePaymentCompleted 결제 완료 이벤트 처리
func (s *orderService) HandlePaymentCompleted(ctx context.Context, evt events.PaymentCompletedEvent) error {
	s.logger.Info("handling payment completed event",
		zap.Int64("orderId", evt.OrderID),
		zap.String("correlationId", evt.CorrelationID))

	order, err := s.findByOrderID(ctx, evt.OrderID, "payment.completed")
	if err != nil {
		return err
	}

	// 상태 전이: PENDING -> STOCK_RESERVING
	return s.transition(ctx, order, domain.OrderStatusStockReserving)
}

// HandlePaymentFailed 결제 실패 이벤트 처리
func (s *orderService) HandlePaymentFailed(ctx context.Context, evt events.PaymentFailedEvent) error {
	s.logger.Warn("handling payment failed event",
		zap.Int64("orderId", evt.OrderID),
		zap.String("reason", evt.Reason))

	order, err := s.findByOrderID(ctx, evt.OrderID, "payment.failed")
	if err != nil {
		return err
	}

	// 주문 취소 (COMPLETED 등 취소 불가능한 상태는 transition 내부에서 무시된다)
	return s.transition(ctx, order, domain.OrderStatusCanceled)
}

// HandleStockReserved 재고 예약 이벤트 처리
func (s *orderService) HandleStockReserved(ctx context.Context, evt events.StockReservedEvent) error {
	s.logger.Info("handling stock reserved event",
		zap.Int64("orderId", evt.OrderID))

	order, err := s.findByOrderID(ctx, evt.OrderID, "stock.reserved")
	if err != nil {
		return err
	}

	// 상태 전이: STOCK_RESERVING -> DELIVERY_PREPARING
	return s.transition(ctx, order, domain.OrderStatusDeliveryPreparing)
}

// HandleStockReservationFailed 재고 예약 실패 이벤트 처리
func (s *orderService) HandleStockReservationFailed(ctx context.Context, evt events.StockReservationFailedEvent) error {
	s.logger.Warn("handling stock reservation failed event",
		zap.Int64("orderId", evt.OrderID),
		zap.String("reason", evt.Reason))

	order, err := s.findByOrderID(ctx, evt.OrderID, "stock.reservation_failed")
	if err != nil {
		return err
	}

	// 주문 실패 (보상 트랜잭션: 결제 환불 필요)
	return s.transition(ctx, order, domain.OrderStatusFailed)
}

// HandleDeliveryStarted 배송 시작 이벤트 처리
func (s *orderService) HandleDeliveryStarted(ctx context.Context, evt events.DeliveryStartedEvent) error {
	s.logger.Info("handling delivery started event",
		zap.Int64("orderId", evt.OrderID))

	order, err := s.findByOrderID(ctx, evt.OrderID, "delivery.started")
	if err != nil {
		return err
	}

	// 상태 전이: DELIVERY_PREPARING -> COMPLETED
	return s.transition(ctx, order, domain.OrderStatusCompleted)
}

// HandleDeliveryFailed 배송 실패 이벤트 처리
func (s *orderService) HandleDeliveryFailed(ctx context.Context, evt events.DeliveryFailedEvent) error {
	s.logger.Warn("handling delivery failed event",
		zap.Int64("orderId", evt.OrderID),
		zap.String("reason", evt.Reason))

	order, err := s.findByOrderID(ctx, evt.OrderID, "delivery.failed")
	if err != nil {
		return err
	}

	// 주문 실패
	return s.transition(ctx, order, domain.OrderStatusFailed)
}
