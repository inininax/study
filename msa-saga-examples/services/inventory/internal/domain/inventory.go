package domain

import "time"

// Inventory 재고 엔티티
type Inventory struct {
	ID                int64     `json:"id"`
	ProductID         int64     `json:"product_id"`
	AvailableQuantity int       `json:"available_quantity"`
	ReservedQuantity  int       `json:"reserved_quantity"`
	Version           int64     `json:"version"`
	CreatedAt         time.Time `json:"created_at"`
	UpdatedAt         time.Time `json:"updated_at"`
}

// CanReserve 재고 예약 가능 여부 확인
func (i *Inventory) CanReserve(quantity int) bool {
	return i.AvailableQuantity >= quantity
}

// Reserve 재고 예약 (낙관적 잠금)
func (i *Inventory) Reserve(quantity int) {
	i.AvailableQuantity -= quantity
	i.ReservedQuantity += quantity
	i.Version++
	i.UpdatedAt = time.Now()
}

// Restore 재고 복구
func (i *Inventory) Restore(quantity int) {
	i.AvailableQuantity += quantity
	i.ReservedQuantity -= quantity
	i.Version++
	i.UpdatedAt = time.Now()
}

