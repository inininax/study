package domain

import "time"

// ReservationStatus 예약 상태
type ReservationStatus string

const (
	ReservationStatusReserved  ReservationStatus = "RESERVED"  // 예약됨
	ReservationStatusConfirmed ReservationStatus = "CONFIRMED" // 확정됨
	ReservationStatusCancelled ReservationStatus = "CANCELLED" // 취소됨
	ReservationStatusExpired   ReservationStatus = "EXPIRED"   // 만료됨
)

// StockReservation 재고 예약 엔티티
type StockReservation struct {
	ID             int64             `json:"id"`
	OrderID        int64             `json:"order_id"`
	ProductID      int64             `json:"product_id"`
	Quantity       int               `json:"quantity"`
	Status         ReservationStatus `json:"status"`
	IdempotencyKey string            `json:"idempotency_key"`
	ExpiredAt      time.Time         `json:"expired_at"`
	CreatedAt      time.Time         `json:"created_at"`
	UpdatedAt      time.Time         `json:"updated_at"`
}

// NewStockReservation 새로운 재고 예약 생성
func NewStockReservation(orderID, productID int64, quantity int, idempotencyKey string) *StockReservation {
	now := time.Now()
	return &StockReservation{
		OrderID:        orderID,
		ProductID:      productID,
		Quantity:       quantity,
		Status:         ReservationStatusReserved,
		IdempotencyKey: idempotencyKey,
		ExpiredAt:      now.Add(30 * time.Minute),
		CreatedAt:      now,
		UpdatedAt:      now,
	}
}

// Cancel 예약 취소
func (r *StockReservation) Cancel() {
	r.Status = ReservationStatusCancelled
	r.UpdatedAt = time.Now()
}

// Confirm 예약 확정
func (r *StockReservation) Confirm() {
	r.Status = ReservationStatusConfirmed
	r.UpdatedAt = time.Now()
}

