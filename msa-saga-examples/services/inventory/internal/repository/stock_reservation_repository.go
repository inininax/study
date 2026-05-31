package repository

import (
	"context"
	"database/sql"

	"github.com/kyungseok/msa-saga-go-examples/common/errors"
	"github.com/kyungseok/msa-saga-go-examples/services/inventory/internal/domain"
)

// StockReservationRepository 재고 예약 저장소 인터페이스
type StockReservationRepository interface {
	// FindByIdempotencyKey 멱등성 키로 예약 조회
	FindByIdempotencyKey(ctx context.Context, idempotencyKey string) (*domain.StockReservation, error)
	
	// Create 재고 예약 생성
	Create(ctx context.Context, tx *sql.Tx, reservation *domain.StockReservation) error
	
	// FindByOrderIDAndStatus 주문 ID와 상태로 예약 조회
	FindByOrderIDAndStatus(ctx context.Context, orderID int64, status domain.ReservationStatus) (*domain.StockReservation, error)
	
	// Update 재고 예약 업데이트
	Update(ctx context.Context, tx *sql.Tx, reservation *domain.StockReservation) error
}

type stockReservationRepository struct {
	db *sql.DB
}

// NewStockReservationRepository 재고 예약 저장소 생성
func NewStockReservationRepository(db *sql.DB) StockReservationRepository {
	return &stockReservationRepository{db: db}
}

// FindByIdempotencyKey 멱등성 키로 예약 조회
func (r *stockReservationRepository) FindByIdempotencyKey(
	ctx context.Context,
	idempotencyKey string,
) (*domain.StockReservation, error) {
	query := `
		SELECT id, order_id, product_id, quantity, status, idempotency_key, expired_at, created_at, updated_at
		FROM stock_reservations
		WHERE idempotency_key = $1
	`
	
	reservation := &domain.StockReservation{}
	err := r.db.QueryRowContext(ctx, query, idempotencyKey).Scan(
		&reservation.ID,
		&reservation.OrderID,
		&reservation.ProductID,
		&reservation.Quantity,
		&reservation.Status,
		&reservation.IdempotencyKey,
		&reservation.ExpiredAt,
		&reservation.CreatedAt,
		&reservation.UpdatedAt,
	)
	
	if err == sql.ErrNoRows {
		return nil, errors.Wrap(errors.ErrCodeNotFound, "stock reservation not found", err)
	}
	if err != nil {
		return nil, errors.Wrap(errors.ErrCodeDatabaseError, "failed to find stock reservation", err)
	}
	
	return reservation, nil
}

// Create 재고 예약 생성
func (r *stockReservationRepository) Create(
	ctx context.Context,
	tx *sql.Tx,
	reservation *domain.StockReservation,
) error {
	query := `
		INSERT INTO stock_reservations (order_id, product_id, quantity, status, idempotency_key, expired_at, created_at, updated_at)
		VALUES ($1, $2, $3, $4, $5, $6, $7, $8)
		RETURNING id, created_at, updated_at
	`
	
	err := tx.QueryRowContext(ctx, query,
		reservation.OrderID,
		reservation.ProductID,
		reservation.Quantity,
		reservation.Status,
		reservation.IdempotencyKey,
		reservation.ExpiredAt,
		reservation.CreatedAt,
		reservation.UpdatedAt,
	).Scan(&reservation.ID, &reservation.CreatedAt, &reservation.UpdatedAt)
	
	if err != nil {
		return errors.Wrap(errors.ErrCodeDatabaseError, "failed to create stock reservation", err)
	}
	
	return nil
}

// FindByOrderIDAndStatus 주문 ID와 상태로 예약 조회
func (r *stockReservationRepository) FindByOrderIDAndStatus(
	ctx context.Context,
	orderID int64,
	status domain.ReservationStatus,
) (*domain.StockReservation, error) {
	query := `
		SELECT id, order_id, product_id, quantity, status, idempotency_key, expired_at, created_at, updated_at
		FROM stock_reservations
		WHERE order_id = $1 AND status = $2
	`
	
	reservation := &domain.StockReservation{}
	err := r.db.QueryRowContext(ctx, query, orderID, status).Scan(
		&reservation.ID,
		&reservation.OrderID,
		&reservation.ProductID,
		&reservation.Quantity,
		&reservation.Status,
		&reservation.IdempotencyKey,
		&reservation.ExpiredAt,
		&reservation.CreatedAt,
		&reservation.UpdatedAt,
	)
	
	if err == sql.ErrNoRows {
		return nil, errors.Wrap(errors.ErrCodeNotFound, "stock reservation not found", err)
	}
	if err != nil {
		return nil, errors.Wrap(errors.ErrCodeDatabaseError, "failed to find stock reservation", err)
	}
	
	return reservation, nil
}

// Update 재고 예약 업데이트
func (r *stockReservationRepository) Update(
	ctx context.Context,
	tx *sql.Tx,
	reservation *domain.StockReservation,
) error {
	query := `
		UPDATE stock_reservations
		SET status = $1, updated_at = $2
		WHERE id = $3
	`
	
	result, err := tx.ExecContext(ctx, query, reservation.Status, reservation.UpdatedAt, reservation.ID)
	if err != nil {
		return errors.Wrap(errors.ErrCodeDatabaseError, "failed to update stock reservation", err)
	}
	
	rows, err := result.RowsAffected()
	if err != nil {
		return errors.Wrap(errors.ErrCodeDatabaseError, "failed to get rows affected", err)
	}
	
	if rows == 0 {
		return errors.Wrap(errors.ErrCodeNotFound, "stock reservation not found", nil)
	}
	
	return nil
}

