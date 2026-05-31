package repository

import (
	"context"
	"database/sql"

	"github.com/kyungseok/msa-saga-go-examples/common/errors"
	"github.com/kyungseok/msa-saga-go-examples/services/inventory/internal/domain"
)

// InventoryRepository 재고 저장소 인터페이스
type InventoryRepository interface {
	// FindByProductIDForUpdate 제품 ID로 재고 조회 (행 잠금)
	FindByProductIDForUpdate(ctx context.Context, tx *sql.Tx, productID int64) (*domain.Inventory, error)
	
	// UpdateWithOptimisticLock 낙관적 잠금으로 재고 업데이트
	UpdateWithOptimisticLock(ctx context.Context, tx *sql.Tx, inventory *domain.Inventory, oldVersion int64) error
	
	// BeginTx 트랜잭션 시작
	BeginTx(ctx context.Context) (*sql.Tx, error)
}

type inventoryRepository struct {
	db *sql.DB
}

// NewInventoryRepository 재고 저장소 생성
func NewInventoryRepository(db *sql.DB) InventoryRepository {
	return &inventoryRepository{db: db}
}

// FindByProductIDForUpdate 제품 ID로 재고 조회 (행 잠금)
func (r *inventoryRepository) FindByProductIDForUpdate(
	ctx context.Context,
	tx *sql.Tx,
	productID int64,
) (*domain.Inventory, error) {
	query := `
		SELECT id, product_id, available_quantity, reserved_quantity, version, created_at, updated_at
		FROM inventory
		WHERE product_id = $1
		FOR UPDATE
	`
	
	inventory := &domain.Inventory{}
	err := tx.QueryRowContext(ctx, query, productID).Scan(
		&inventory.ID,
		&inventory.ProductID,
		&inventory.AvailableQuantity,
		&inventory.ReservedQuantity,
		&inventory.Version,
		&inventory.CreatedAt,
		&inventory.UpdatedAt,
	)
	
	if err == sql.ErrNoRows {
		return nil, errors.Wrap(errors.ErrCodeNotFound, "inventory not found", err)
	}
	if err != nil {
		return nil, errors.Wrap(errors.ErrCodeDatabaseError, "failed to find inventory", err)
	}
	
	return inventory, nil
}

// UpdateWithOptimisticLock 낙관적 잠금으로 재고 업데이트
func (r *inventoryRepository) UpdateWithOptimisticLock(
	ctx context.Context,
	tx *sql.Tx,
	inventory *domain.Inventory,
	oldVersion int64,
) error {
	query := `
		UPDATE inventory
		SET available_quantity = $1,
		    reserved_quantity = $2,
		    version = $3,
		    updated_at = $4
		WHERE product_id = $5 AND version = $6
	`
	
	result, err := tx.ExecContext(ctx, query,
		inventory.AvailableQuantity,
		inventory.ReservedQuantity,
		inventory.Version,
		inventory.UpdatedAt,
		inventory.ProductID,
		oldVersion,
	)
	
	if err != nil {
		return errors.Wrap(errors.ErrCodeDatabaseError, "failed to update inventory", err)
	}
	
	rows, err := result.RowsAffected()
	if err != nil {
		return errors.Wrap(errors.ErrCodeDatabaseError, "failed to get rows affected", err)
	}
	
	if rows == 0 {
		return errors.Wrap(errors.ErrCodeConflict, "version conflict - inventory was modified", nil)
	}
	
	return nil
}

// BeginTx 트랜잭션 시작
func (r *inventoryRepository) BeginTx(ctx context.Context) (*sql.Tx, error) {
	tx, err := r.db.BeginTx(ctx, nil)
	if err != nil {
		return nil, errors.Wrap(errors.ErrCodeDatabaseError, "failed to begin transaction", err)
	}
	return tx, nil
}

