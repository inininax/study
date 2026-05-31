package repository

import (
	"context"
	"database/sql"
	"encoding/json"

	"github.com/kyungseok/msa-saga-go-examples/common/errors"
	"github.com/kyungseok/msa-saga-go-examples/common/events"
)

// OutboxRepository 아웃박스 저장소 인터페이스
type OutboxRepository interface {
	// InsertEvent 아웃박스 이벤트 추가
	InsertEvent(ctx context.Context, tx *sql.Tx, aggregateType string, aggregateID int64, event events.Event) error
	
	// GetPendingEvents 대기 중인 이벤트 조회
	GetPendingEvents(ctx context.Context, limit int) ([]*OutboxEvent, error)
	
	// MarkAsSent 이벤트를 전송 완료로 표시
	MarkAsSent(ctx context.Context, id int64) error
}

// OutboxEvent 아웃박스 이벤트
type OutboxEvent struct {
	ID            int64           `json:"id"`
	AggregateType string          `json:"aggregate_type"`
	AggregateID   int64           `json:"aggregate_id"`
	EventType     string          `json:"event_type"`
	Payload       json.RawMessage `json:"payload"`
	Status        string          `json:"status"`
}

type outboxRepository struct {
	db *sql.DB
}

// NewOutboxRepository 아웃박스 저장소 생성
func NewOutboxRepository(db *sql.DB) OutboxRepository {
	return &outboxRepository{db: db}
}

// InsertEvent 아웃박스 이벤트 추가
func (r *outboxRepository) InsertEvent(
	ctx context.Context,
	tx *sql.Tx,
	aggregateType string,
	aggregateID int64,
	event events.Event,
) error {
	payload, err := json.Marshal(event)
	if err != nil {
		return errors.Wrap(errors.ErrCodeInternalError, "failed to marshal event", err)
	}
	
	query := `
		INSERT INTO outbox_events (aggregate_type, aggregate_id, event_type, payload, status, created_at)
		VALUES ($1, $2, $3, $4, 'PENDING', NOW())
	`
	
	_, err = tx.ExecContext(ctx, query, aggregateType, aggregateID, event.GetEventType(), payload)
	if err != nil {
		return errors.Wrap(errors.ErrCodeDatabaseError, "failed to insert outbox event", err)
	}
	
	return nil
}

// GetPendingEvents 대기 중인 이벤트 조회
func (r *outboxRepository) GetPendingEvents(ctx context.Context, limit int) ([]*OutboxEvent, error) {
	query := `
		SELECT id, aggregate_type, aggregate_id, event_type, payload, status
		FROM outbox_events
		WHERE status = 'PENDING'
		ORDER BY created_at
		LIMIT $1
	`
	
	rows, err := r.db.QueryContext(ctx, query, limit)
	if err != nil {
		return nil, errors.Wrap(errors.ErrCodeDatabaseError, "failed to query pending events", err)
	}
	defer rows.Close()
	
	var events []*OutboxEvent
	for rows.Next() {
		event := &OutboxEvent{}
		err := rows.Scan(
			&event.ID,
			&event.AggregateType,
			&event.AggregateID,
			&event.EventType,
			&event.Payload,
			&event.Status,
		)
		if err != nil {
			return nil, errors.Wrap(errors.ErrCodeDatabaseError, "failed to scan event", err)
		}
		events = append(events, event)
	}
	
	if err = rows.Err(); err != nil {
		return nil, errors.Wrap(errors.ErrCodeDatabaseError, "rows iteration error", err)
	}
	
	return events, nil
}

// MarkAsSent 이벤트를 전송 완료로 표시
func (r *outboxRepository) MarkAsSent(ctx context.Context, id int64) error {
	query := `
		UPDATE outbox_events
		SET status = 'SENT', sent_at = NOW()
		WHERE id = $1
	`
	
	_, err := r.db.ExecContext(ctx, query, id)
	if err != nil {
		return errors.Wrap(errors.ErrCodeDatabaseError, "failed to mark event as sent", err)
	}
	
	return nil
}

