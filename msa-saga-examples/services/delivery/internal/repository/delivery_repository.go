package repository

import (
	"context"
	"database/sql"

	"github.com/kyungseok/msa-saga-go-examples/common/errors"
	"github.com/kyungseok/msa-saga-go-examples/services/delivery/internal/domain"
)

// DeliveryRepository 배송 저장소 인터페이스
type DeliveryRepository interface {
	// FindByIdempotencyKey 멱등성 키로 배송 조회
	FindByIdempotencyKey(ctx context.Context, idempotencyKey string) (*domain.Delivery, error)
	
	// Create 배송 생성
	Create(ctx context.Context, tx *sql.Tx, delivery *domain.Delivery) error
	
	// Update 배송 업데이트
	Update(ctx context.Context, tx *sql.Tx, delivery *domain.Delivery) error
	
	// FindByID ID로 배송 조회
	FindByID(ctx context.Context, id int64) (*domain.Delivery, error)
	
	// BeginTx 트랜잭션 시작
	BeginTx(ctx context.Context) (*sql.Tx, error)
}

type deliveryRepository struct {
	db *sql.DB
}

// NewDeliveryRepository 배송 저장소 생성
func NewDeliveryRepository(db *sql.DB) DeliveryRepository {
	return &deliveryRepository{db: db}
}

// FindByIdempotencyKey 멱등성 키로 배송 조회
func (r *deliveryRepository) FindByIdempotencyKey(ctx context.Context, idempotencyKey string) (*domain.Delivery, error) {
	query := `
		SELECT id, order_id, address, status, tracking_number, carrier, idempotency_key, created_at, updated_at
		FROM deliveries
		WHERE idempotency_key = $1
	`
	
	delivery := &domain.Delivery{}
	err := r.db.QueryRowContext(ctx, query, idempotencyKey).Scan(
		&delivery.ID,
		&delivery.OrderID,
		&delivery.Address,
		&delivery.Status,
		&delivery.TrackingNumber,
		&delivery.Carrier,
		&delivery.IdempotencyKey,
		&delivery.CreatedAt,
		&delivery.UpdatedAt,
	)
	
	if err == sql.ErrNoRows {
		return nil, errors.Wrap(errors.ErrCodeNotFound, "delivery not found", err)
	}
	if err != nil {
		return nil, errors.Wrap(errors.ErrCodeDatabaseError, "failed to find delivery", err)
	}
	
	return delivery, nil
}

// Create 배송 생성
func (r *deliveryRepository) Create(ctx context.Context, tx *sql.Tx, delivery *domain.Delivery) error {
	query := `
		INSERT INTO deliveries (order_id, address, status, idempotency_key, tracking_number, carrier, created_at, updated_at)
		VALUES ($1, $2, $3, $4, $5, $6, $7, $8)
		RETURNING id, created_at, updated_at
	`
	
	err := tx.QueryRowContext(ctx, query,
		delivery.OrderID,
		delivery.Address,
		delivery.Status,
		delivery.IdempotencyKey,
		delivery.TrackingNumber,
		delivery.Carrier,
		delivery.CreatedAt,
		delivery.UpdatedAt,
	).Scan(&delivery.ID, &delivery.CreatedAt, &delivery.UpdatedAt)
	
	if err != nil {
		return errors.Wrap(errors.ErrCodeDatabaseError, "failed to create delivery", err)
	}
	
	return nil
}

// Update 배송 업데이트
func (r *deliveryRepository) Update(ctx context.Context, tx *sql.Tx, delivery *domain.Delivery) error {
	query := `
		UPDATE deliveries
		SET status = $1, updated_at = $2
		WHERE id = $3
	`
	
	result, err := tx.ExecContext(ctx, query, delivery.Status, delivery.UpdatedAt, delivery.ID)
	if err != nil {
		return errors.Wrap(errors.ErrCodeDatabaseError, "failed to update delivery", err)
	}
	
	rows, err := result.RowsAffected()
	if err != nil {
		return errors.Wrap(errors.ErrCodeDatabaseError, "failed to get rows affected", err)
	}
	
	if rows == 0 {
		return errors.Wrap(errors.ErrCodeNotFound, "delivery not found", nil)
	}
	
	return nil
}

// FindByID ID로 배송 조회
func (r *deliveryRepository) FindByID(ctx context.Context, id int64) (*domain.Delivery, error) {
	query := `
		SELECT id, order_id, address, status, tracking_number, carrier, idempotency_key, created_at, updated_at
		FROM deliveries
		WHERE id = $1
	`
	
	delivery := &domain.Delivery{}
	err := r.db.QueryRowContext(ctx, query, id).Scan(
		&delivery.ID,
		&delivery.OrderID,
		&delivery.Address,
		&delivery.Status,
		&delivery.TrackingNumber,
		&delivery.Carrier,
		&delivery.IdempotencyKey,
		&delivery.CreatedAt,
		&delivery.UpdatedAt,
	)
	
	if err == sql.ErrNoRows {
		return nil, errors.Wrap(errors.ErrCodeNotFound, "delivery not found", err)
	}
	if err != nil {
		return nil, errors.Wrap(errors.ErrCodeDatabaseError, "failed to find delivery", err)
	}
	
	return delivery, nil
}

// BeginTx 트랜잭션 시작
func (r *deliveryRepository) BeginTx(ctx context.Context) (*sql.Tx, error) {
	tx, err := r.db.BeginTx(ctx, nil)
	if err != nil {
		return nil, errors.Wrap(errors.ErrCodeDatabaseError, "failed to begin transaction", err)
	}
	return tx, nil
}

