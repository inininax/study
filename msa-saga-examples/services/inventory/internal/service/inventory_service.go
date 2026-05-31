package service

import (
	"context"
	"database/sql"
	"fmt"
	"time"

	"github.com/google/uuid"
	"github.com/kyungseok/msa-saga-go-examples/common/errors"
	"github.com/kyungseok/msa-saga-go-examples/common/events"
	"github.com/kyungseok/msa-saga-go-examples/services/inventory/internal/domain"
	"github.com/kyungseok/msa-saga-go-examples/services/inventory/internal/repository"
	"go.uber.org/zap"
)

// InventoryService 재고 서비스 인터페이스
type InventoryService interface {
	HandlePaymentCompleted(ctx context.Context, evt events.PaymentCompletedEvent) error
	HandlePaymentRefunded(ctx context.Context, evt events.PaymentRefundedEvent) error
}

type inventoryService struct {
	inventoryRepo    repository.InventoryRepository
	reservationRepo  repository.StockReservationRepository
	outboxRepo       repository.OutboxRepository
	logger           *zap.Logger
}

// NewInventoryService 재고 서비스 생성
func NewInventoryService(
	inventoryRepo repository.InventoryRepository,
	reservationRepo repository.StockReservationRepository,
	outboxRepo repository.OutboxRepository,
	logger *zap.Logger,
) InventoryService {
	return &inventoryService{
		inventoryRepo:   inventoryRepo,
		reservationRepo: reservationRepo,
		outboxRepo:      outboxRepo,
		logger:          logger,
	}
}

// HandlePaymentCompleted 결제 완료 이벤트 처리 (재고 예약)
func (s *inventoryService) HandlePaymentCompleted(ctx context.Context, evt events.PaymentCompletedEvent) error {
	s.logger.Info("handling payment completed event - reserving stock",
		zap.Int64("orderId", evt.OrderID))

	// 멱등성 키 생성
	idempotencyKey := fmt.Sprintf("stock-reservation-%d-%s", evt.OrderID, evt.EventID)

	// 이미 처리된 요청인지 확인
	existingReservation, err := s.reservationRepo.FindByIdempotencyKey(ctx, idempotencyKey)
	if err == nil && existingReservation != nil {
		s.logger.Info("stock already reserved",
			zap.String("idempotencyKey", idempotencyKey),
			zap.Int64("reservationId", existingReservation.ID))
		return nil
	}

	// NotFound 에러가 아니면 실패
	if err != nil && !errors.IsCode(err, errors.ErrCodeNotFound) {
		return err
	}

	// 트랜잭션 시작
	tx, err := s.inventoryRepo.BeginTx(ctx)
	if err != nil {
		return err
	}
	defer tx.Rollback()

	// 재고 확인 및 예약 (단순화: productID=1로 가정)
	productID := int64(1)
	quantity := 1 // evt.Quantity 사용 가능

	// 재고 조회 (FOR UPDATE)
	inventory, err := s.inventoryRepo.FindByProductIDForUpdate(ctx, tx, productID)
	if err != nil {
		return s.publishStockReservationFailed(ctx, tx, evt, "product not found")
	}

	// 재고 부족 체크
	if !inventory.CanReserve(quantity) {
		return s.publishStockReservationFailed(ctx, tx, evt, "insufficient stock")
	}

	// 재고 예약 (Optimistic Lock)
	oldVersion := inventory.Version
	inventory.Reserve(quantity)

	err = s.inventoryRepo.UpdateWithOptimisticLock(ctx, tx, inventory, oldVersion)
	if err != nil {
		if errors.IsCode(err, errors.ErrCodeConflict) {
			return s.publishStockReservationFailed(ctx, tx, evt, "version conflict")
		}
		return err
	}

	// 재고 예약 기록 생성
	reservation := domain.NewStockReservation(evt.OrderID, productID, quantity, idempotencyKey)
	if err := s.reservationRepo.Create(ctx, tx, reservation); err != nil {
		return err
	}

	// StockReserved 이벤트 발행
	now := time.Now()
	stockReservedEvt := events.StockReservedEvent{
		BaseEvent: events.BaseEvent{
			EventID:       uuid.New().String(),
			EventType:     events.EventStockReserved,
			SchemaVersion: 1,
			OccurredAt:    now,
			CorrelationID: evt.CorrelationID,
		},
		OrderID:       evt.OrderID,
		ReservationID: reservation.ID,
		Quantity:      quantity,
	}

	if err := s.outboxRepo.InsertEvent(ctx, tx, "stock_reservation", reservation.ID, stockReservedEvt); err != nil {
		return err
	}

	// 트랜잭션 커밋
	if err := tx.Commit(); err != nil {
		return errors.Wrap(errors.ErrCodeDatabaseError, "failed to commit transaction", err)
	}

	s.logger.Info("stock reserved successfully",
		zap.Int64("reservationId", reservation.ID),
		zap.Int64("orderId", evt.OrderID))

	return nil
}

// HandlePaymentRefunded 결제 환불 이벤트 처리 (재고 복구 - 보상 트랜잭션)
func (s *inventoryService) HandlePaymentRefunded(ctx context.Context, evt events.PaymentRefundedEvent) error {
	s.logger.Warn("handling payment refunded event - restoring stock",
		zap.Int64("orderId", evt.OrderID))

	// 해당 주문의 재고 예약 조회
	reservation, err := s.reservationRepo.FindByOrderIDAndStatus(ctx, evt.OrderID, domain.ReservationStatusReserved)
	if err != nil {
		if errors.IsCode(err, errors.ErrCodeNotFound) {
			s.logger.Warn("stock reservation not found - may already be restored",
				zap.Int64("orderId", evt.OrderID))
			return nil
		}
		return err
	}

	// 트랜잭션 시작
	tx, err := s.inventoryRepo.BeginTx(ctx)
	if err != nil {
		return err
	}
	defer tx.Rollback()

	// 재고 조회 (FOR UPDATE)
	inventory, err := s.inventoryRepo.FindByProductIDForUpdate(ctx, tx, reservation.ProductID)
	if err != nil {
		return err
	}

	// 재고 복구
	oldVersion := inventory.Version
	inventory.Restore(reservation.Quantity)

	if err := s.inventoryRepo.UpdateWithOptimisticLock(ctx, tx, inventory, oldVersion); err != nil {
		return err
	}

	// 예약 상태 업데이트
	reservation.Cancel()
	if err := s.reservationRepo.Update(ctx, tx, reservation); err != nil {
		return err
	}

	// StockRestored 이벤트 발행
	now := time.Now()
	stockRestoredEvt := events.StockRestoredEvent{
		BaseEvent: events.BaseEvent{
			EventID:       uuid.New().String(),
			EventType:     events.EventStockRestored,
			SchemaVersion: 1,
			OccurredAt:    now,
			CorrelationID: evt.CorrelationID,
		},
		OrderID:       evt.OrderID,
		ReservationID: reservation.ID,
		Quantity:      reservation.Quantity,
	}

	if err := s.outboxRepo.InsertEvent(ctx, tx, "stock_reservation", reservation.ID, stockRestoredEvt); err != nil {
		return err
	}

	if err := tx.Commit(); err != nil {
		return errors.Wrap(errors.ErrCodeDatabaseError, "failed to commit transaction", err)
	}

	s.logger.Info("stock restored successfully",
		zap.Int64("reservationId", reservation.ID),
		zap.Int64("orderId", evt.OrderID))

	return nil
}

func (s *inventoryService) publishStockReservationFailed(
	ctx context.Context,
	tx *sql.Tx,
	evt events.PaymentCompletedEvent,
	reason string,
) error {
	now := time.Now()
	failedEvt := events.StockReservationFailedEvent{
		BaseEvent: events.BaseEvent{
			EventID:       uuid.New().String(),
			EventType:     events.EventStockReservationFailed,
			SchemaVersion: 1,
			OccurredAt:    now,
			CorrelationID: evt.CorrelationID,
		},
		OrderID:  evt.OrderID,
		Quantity: 1,
		Reason:   reason,
	}

	if err := s.outboxRepo.InsertEvent(ctx, tx, "order", evt.OrderID, failedEvt); err != nil {
		return err
	}

	if err := tx.Commit(); err != nil {
		return errors.Wrap(errors.ErrCodeDatabaseError, "failed to commit transaction", err)
	}

	s.logger.Warn("stock reservation failed event published",
		zap.Int64("orderId", evt.OrderID),
		zap.String("reason", reason))

	return fmt.Errorf("stock reservation failed: %s", reason)
}
