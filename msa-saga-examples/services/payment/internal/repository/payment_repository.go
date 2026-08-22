package repository

import (
	"context"
	"database/sql"
	"fmt"

	"github.com/kyungseok/msa-saga-go-examples/services/payment/internal/domain"
	"github.com/lib/pq"
)

// PaymentRepository 결제 레포지토리 인터페이스
type PaymentRepository interface {
	CreateTx(ctx context.Context, tx *sql.Tx, payment *domain.Payment) error
	FindByID(ctx context.Context, id int64) (*domain.Payment, error)
	FindByOrderID(ctx context.Context, orderID int64) (*domain.Payment, error)
	FindByIdempotencyKey(ctx context.Context, key string) (*domain.Payment, error)
	UpdateStatusTx(ctx context.Context, tx *sql.Tx, id int64, status domain.PaymentStatus, reason string) error
}

type paymentRepository struct {
	db *sql.DB
}

// NewPaymentRepository 결제 레포지토리 생성
func NewPaymentRepository(db *sql.DB) PaymentRepository {
	return &paymentRepository{db: db}
}

const createPaymentQuery = `
	INSERT INTO payments (order_id, amount, payment_type, status, idempotency_key, payment_gateway_tx_id, created_at, updated_at)
	VALUES ($1, $2, $3, $4, $5, $6, $7, $8)
	RETURNING id
`

func scanCreatePaymentErr(err error) error {
	if pqErr, ok := err.(*pq.Error); ok && pqErr.Code == "23505" {
		return fmt.Errorf("duplicate idempotency key: %w", err)
	}
	return fmt.Errorf("failed to create payment: %w", err)
}

const selectPaymentColumns = `
	SELECT id, order_id, amount, payment_type, status, idempotency_key, payment_gateway_tx_id, reason, created_at, updated_at
	FROM payments
`

func scanPaymentRow(row *sql.Row) (*domain.Payment, error) {
	payment := &domain.Payment{}
	var reason sql.NullString

	err := row.Scan(
		&payment.ID,
		&payment.OrderID,
		&payment.Amount,
		&payment.PaymentType,
		&payment.Status,
		&payment.IdempotencyKey,
		&payment.PaymentGatewayTxID,
		&reason,
		&payment.CreatedAt,
		&payment.UpdatedAt,
	)

	if err == sql.ErrNoRows {
		return nil, err
	}
	if err != nil {
		return nil, fmt.Errorf("failed to find payment: %w", err)
	}

	if reason.Valid {
		payment.Reason = reason.String
	}

	return payment, nil
}

// CreateTx 트랜잭션 내에서 결제 생성
func (r *paymentRepository) CreateTx(ctx context.Context, tx *sql.Tx, payment *domain.Payment) error {
	err := tx.QueryRowContext(
		ctx,
		createPaymentQuery,
		payment.OrderID,
		payment.Amount,
		payment.PaymentType,
		payment.Status,
		payment.IdempotencyKey,
		payment.PaymentGatewayTxID,
		payment.CreatedAt,
		payment.UpdatedAt,
	).Scan(&payment.ID)

	if err != nil {
		return scanCreatePaymentErr(err)
	}

	return nil
}

// FindByID ID로 결제 조회 (미존재 시 sql.ErrNoRows 반환)
func (r *paymentRepository) FindByID(ctx context.Context, id int64) (*domain.Payment, error) {
	payment, err := scanPaymentRow(r.db.QueryRowContext(ctx, selectPaymentColumns+" WHERE id = $1", id))
	if err == sql.ErrNoRows {
		return nil, fmt.Errorf("payment not found: %d: %w", id, sql.ErrNoRows)
	}
	if err != nil {
		return nil, err
	}
	return payment, nil
}

// FindByOrderID OrderID로 결제 조회 (미존재 시 sql.ErrNoRows 반환)
func (r *paymentRepository) FindByOrderID(ctx context.Context, orderID int64) (*domain.Payment, error) {
	query := selectPaymentColumns + `
		WHERE order_id = $1
		ORDER BY created_at DESC
		LIMIT 1
	`
	payment, err := scanPaymentRow(r.db.QueryRowContext(ctx, query, orderID))
	if err == sql.ErrNoRows {
		return nil, fmt.Errorf("payment not found for order: %d: %w", orderID, sql.ErrNoRows)
	}
	if err != nil {
		return nil, err
	}
	return payment, nil
}

// FindByIdempotencyKey 멱등성 키로 결제 조회 (미존재 시 sql.ErrNoRows 반환)
func (r *paymentRepository) FindByIdempotencyKey(ctx context.Context, key string) (*domain.Payment, error) {
	payment, err := scanPaymentRow(r.db.QueryRowContext(ctx, selectPaymentColumns+" WHERE idempotency_key = $1", key))
	if err == sql.ErrNoRows {
		return nil, fmt.Errorf("payment not found with idempotency key: %s: %w", key, sql.ErrNoRows)
	}
	if err != nil {
		return nil, err
	}
	return payment, nil
}

// UpdateStatusTx 트랜잭션 내에서 결제 상태 업데이트
func (r *paymentRepository) UpdateStatusTx(ctx context.Context, tx *sql.Tx, id int64, status domain.PaymentStatus, reason string) error {
	query := `
		UPDATE payments
		SET status = $1, reason = $2, updated_at = NOW()
		WHERE id = $3
	`

	_, err := tx.ExecContext(ctx, query, status, reason, id)
	if err != nil {
		return fmt.Errorf("failed to update payment status: %w", err)
	}

	return nil
}
