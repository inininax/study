package service

import (
	"context"
	"fmt"
	"time"

	"github.com/google/uuid"
	"github.com/kyungseok/msa-saga-go-examples/common/errors"
	"github.com/kyungseok/msa-saga-go-examples/common/events"
	"github.com/kyungseok/msa-saga-go-examples/services/delivery/internal/domain"
	"github.com/kyungseok/msa-saga-go-examples/services/delivery/internal/repository"
	"go.uber.org/zap"
)

// DeliveryService 배송 서비스 인터페이스
type DeliveryService interface {
	HandleStockReserved(ctx context.Context, evt events.StockReservedEvent) error
}

type deliveryService struct {
	deliveryRepo repository.DeliveryRepository
	outboxRepo   repository.OutboxRepository
	logger       *zap.Logger
}

// NewDeliveryService 배송 서비스 생성
func NewDeliveryService(
	deliveryRepo repository.DeliveryRepository,
	outboxRepo repository.OutboxRepository,
	logger *zap.Logger,
) DeliveryService {
	return &deliveryService{
		deliveryRepo: deliveryRepo,
		outboxRepo:   outboxRepo,
		logger:       logger,
	}
}

// HandleStockReserved 재고 예약 이벤트 처리 (배송 시작)
func (s *deliveryService) HandleStockReserved(ctx context.Context, evt events.StockReservedEvent) error {
	s.logger.Info("handling stock reserved event - starting delivery",
		zap.Int64("orderId", evt.OrderID))

	// 멱등성 키 생성
	idempotencyKey := fmt.Sprintf("delivery-%d-%s", evt.OrderID, evt.EventID)

	// 이미 처리된 요청인지 확인
	existingDelivery, err := s.deliveryRepo.FindByIdempotencyKey(ctx, idempotencyKey)
	if err == nil && existingDelivery != nil {
		s.logger.Info("delivery already started",
			zap.String("idempotencyKey", idempotencyKey),
			zap.Int64("deliveryId", existingDelivery.ID))
		return nil
	}

	// NotFound 에러가 아니면 실패
	if err != nil && !errors.IsCode(err, errors.ErrCodeNotFound) {
		return err
	}

	// 트랜잭션 시작
	tx, err := s.deliveryRepo.BeginTx(ctx)
	if err != nil {
		return err
	}
	defer tx.Rollback()

	// 배송 정보 생성
	trackingNumber := fmt.Sprintf("TRK-%d-%d", evt.OrderID, time.Now().Unix())
	address := "서울시 강남구 테헤란로 123" // 실제로는 주문 정보에서 가져와야 함
	carrier := "CJ대한통운"

	delivery := domain.NewDelivery(evt.OrderID, address, trackingNumber, carrier, idempotencyKey)

	if err := s.deliveryRepo.Create(ctx, tx, delivery); err != nil {
		return err
	}

	// DeliveryStarted 이벤트 발행
	now := time.Now()
	deliveryStartedEvt := events.DeliveryStartedEvent{
		BaseEvent: events.BaseEvent{
			EventID:       uuid.New().String(),
			EventType:     events.EventDeliveryStarted,
			SchemaVersion: 1,
			OccurredAt:    now,
			CorrelationID: evt.CorrelationID,
		},
		OrderID:    evt.OrderID,
		DeliveryID: delivery.ID,
		Address:    address,
	}

	if err := s.outboxRepo.InsertEvent(ctx, tx, "delivery", delivery.ID, deliveryStartedEvt); err != nil {
		return err
	}

	// 트랜잭션 커밋
	if err := tx.Commit(); err != nil {
		return errors.Wrap(errors.ErrCodeDatabaseError, "failed to commit transaction", err)
	}

	s.logger.Info("delivery started successfully",
		zap.Int64("deliveryId", delivery.ID),
		zap.Int64("orderId", evt.OrderID),
		zap.String("trackingNumber", trackingNumber))

	return nil
}
