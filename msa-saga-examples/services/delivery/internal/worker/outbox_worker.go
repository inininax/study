package worker

import (
	"context"
	"encoding/json"
	"time"

	"github.com/kyungseok/msa-saga-go-examples/common/messaging"
	"github.com/kyungseok/msa-saga-go-examples/services/delivery/internal/repository"
	"go.uber.org/zap"
)

// OutboxWorker 아웃박스 워커
type OutboxWorker struct {
	outboxRepo repository.OutboxRepository
	publisher  messaging.Publisher
	logger     *zap.Logger
	interval   time.Duration
}

// NewOutboxWorker 아웃박스 워커 생성
func NewOutboxWorker(
	outboxRepo repository.OutboxRepository,
	publisher messaging.Publisher,
	logger *zap.Logger,
	interval time.Duration,
) *OutboxWorker {
	return &OutboxWorker{
		outboxRepo: outboxRepo,
		publisher:  publisher,
		logger:     logger,
		interval:   interval,
	}
}

// Start 워커 시작
func (w *OutboxWorker) Start(ctx context.Context) {
	ticker := time.NewTicker(w.interval)
	defer ticker.Stop()

	w.logger.Info("outbox worker started", zap.Duration("interval", w.interval))

	for {
		select {
		case <-ctx.Done():
			w.logger.Info("outbox worker stopped")
			return
		case <-ticker.C:
			if err := w.processEvents(ctx); err != nil {
				w.logger.Error("failed to process events", zap.Error(err))
			}
		}
	}
}

func (w *OutboxWorker) processEvents(ctx context.Context) error {
	events, err := w.outboxRepo.GetPendingEvents(ctx, 100)
	if err != nil {
		return err
	}

	for _, event := range events {
		if err := w.publishEvent(ctx, event); err != nil {
			w.logger.Error("failed to publish event",
				zap.Int64("eventId", event.ID),
				zap.String("eventType", event.EventType),
				zap.Error(err))
			continue
		}

		if err := w.outboxRepo.MarkAsSent(ctx, event.ID); err != nil {
			w.logger.Error("failed to mark event as sent",
				zap.Int64("eventId", event.ID),
				zap.Error(err))
		}
	}

	return nil
}

func (w *OutboxWorker) publishEvent(ctx context.Context, event *repository.OutboxEvent) error {
	if err := w.publisher.Publish(ctx, event.EventType, "", json.RawMessage(event.Payload)); err != nil {
		return err
	}

	w.logger.Debug("event published",
		zap.Int64("eventId", event.ID),
		zap.String("eventType", event.EventType))

	return nil
}

