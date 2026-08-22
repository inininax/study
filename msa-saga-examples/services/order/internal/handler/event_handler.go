package handler

import (
	"context"
	"encoding/json"
	"fmt"
	"time"

	commonerrors "github.com/kyungseok/msa-saga-go-examples/common/errors"
	"github.com/kyungseok/msa-saga-go-examples/common/events"
	"github.com/kyungseok/msa-saga-go-examples/common/idempotency"
	"github.com/kyungseok/msa-saga-go-examples/common/messaging"
	"github.com/kyungseok/msa-saga-go-examples/services/order/internal/service"
	"go.uber.org/zap"
)

// idempotentEvent EventID를 가진 이벤트 공통 제약
type idempotentEvent interface {
	GetEventID() string
}

// EventHandler 이벤트 핸들러
type EventHandler struct {
	orderService service.OrderService
	idemStore    idempotency.Store
	logger       *zap.Logger
}

// NewEventHandler 이벤트 핸들러 생성
func NewEventHandler(
	orderService service.OrderService,
	idemStore idempotency.Store,
	logger *zap.Logger,
) *EventHandler {
	return &EventHandler{
		orderService: orderService,
		idemStore:    idemStore,
		logger:       logger,
	}
}

// HandleMessage 메시지 처리
func (h *EventHandler) HandleMessage(ctx context.Context, msg *messaging.Message) error {
	h.logger.Info("received message",
		zap.String("topic", msg.Topic),
		zap.Int64("offset", msg.Offset))

	// 이벤트 타입에 따라 분기
	switch events.EventType(msg.Topic) {
	case events.EventPaymentCompleted:
		return h.handlePaymentCompleted(ctx, msg)
	case events.EventPaymentFailed:
		return h.handlePaymentFailed(ctx, msg)
	case events.EventStockReserved:
		return h.handleStockReserved(ctx, msg)
	case events.EventStockReservationFailed:
		return h.handleStockReservationFailed(ctx, msg)
	case events.EventDeliveryStarted:
		return h.handleDeliveryStarted(ctx, msg)
	case events.EventDeliveryFailed:
		return h.handleDeliveryFailed(ctx, msg)
	default:
		h.logger.Warn("unknown event type", zap.String("topic", msg.Topic))
		return nil
	}
}

// process 모든 핸들러가 공유하는 처리 파이프라인 (fail-closed 멱등성).
//   - JSON 파싱 실패 → MalformedMessage 비즈니스 에러 (컨슈머가 마킹 후 건너뜀)
//   - IsProcessed 조회 실패 → 에러 반환 (마킹하지 않아 재전달로 정합성 확보)
//   - 이미 처리됨 → nil
//   - 처리 실패 → 에러 반환 (재전달)
//   - Reserve(처리 완료 표시) 실패 → 에러 반환 (재전달되어도 핸들러는 멱등하므로 안전)
func process[T idempotentEvent](
	ctx context.Context,
	logger *zap.Logger,
	idemStore idempotency.Store,
	msg *messaging.Message,
	handle func(context.Context, T) error,
) error {
	var evt T
	if err := json.Unmarshal(msg.Value, &evt); err != nil {
		logger.Error("malformed message payload",
			zap.String("topic", msg.Topic),
			zap.Int64("offset", msg.Offset),
			zap.Error(err))
		return commonerrors.Wrap(commonerrors.ErrCodeMalformedMessage, "failed to unmarshal event payload", err)
	}

	processed, err := idemStore.IsProcessed(ctx, evt.GetEventID())
	if err != nil {
		logger.Error("idempotency check failed",
			zap.String("eventId", evt.GetEventID()),
			zap.Error(err))
		return fmt.Errorf("idempotency check failed for event %s: %w", evt.GetEventID(), err)
	}
	if processed {
		logger.Info("event already processed", zap.String("eventId", evt.GetEventID()))
		return nil
	}

	if err := handle(ctx, evt); err != nil {
		return err
	}

	if _, err := idemStore.Reserve(ctx, evt.GetEventID(), 24*time.Hour); err != nil {
		logger.Error("failed to mark event processed",
			zap.String("eventId", evt.GetEventID()),
			zap.Error(err))
		return fmt.Errorf("failed to mark event %s processed: %w", evt.GetEventID(), err)
	}
	return nil
}

func (h *EventHandler) handlePaymentCompleted(ctx context.Context, msg *messaging.Message) error {
	return process(ctx, h.logger, h.idemStore, msg, func(ctx context.Context, evt events.PaymentCompletedEvent) error {
		return h.orderService.HandlePaymentCompleted(ctx, evt)
	})
}

func (h *EventHandler) handlePaymentFailed(ctx context.Context, msg *messaging.Message) error {
	return process(ctx, h.logger, h.idemStore, msg, func(ctx context.Context, evt events.PaymentFailedEvent) error {
		return h.orderService.HandlePaymentFailed(ctx, evt)
	})
}

func (h *EventHandler) handleStockReserved(ctx context.Context, msg *messaging.Message) error {
	return process(ctx, h.logger, h.idemStore, msg, func(ctx context.Context, evt events.StockReservedEvent) error {
		return h.orderService.HandleStockReserved(ctx, evt)
	})
}

func (h *EventHandler) handleStockReservationFailed(ctx context.Context, msg *messaging.Message) error {
	return process(ctx, h.logger, h.idemStore, msg, func(ctx context.Context, evt events.StockReservationFailedEvent) error {
		return h.orderService.HandleStockReservationFailed(ctx, evt)
	})
}

func (h *EventHandler) handleDeliveryStarted(ctx context.Context, msg *messaging.Message) error {
	return process(ctx, h.logger, h.idemStore, msg, func(ctx context.Context, evt events.DeliveryStartedEvent) error {
		return h.orderService.HandleDeliveryStarted(ctx, evt)
	})
}

func (h *EventHandler) handleDeliveryFailed(ctx context.Context, msg *messaging.Message) error {
	return process(ctx, h.logger, h.idemStore, msg, func(ctx context.Context, evt events.DeliveryFailedEvent) error {
		return h.orderService.HandleDeliveryFailed(ctx, evt)
	})
}
