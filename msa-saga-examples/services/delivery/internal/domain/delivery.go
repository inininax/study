package domain

import "time"

// DeliveryStatus 배송 상태
type DeliveryStatus string

const (
	DeliveryStatusPreparing  DeliveryStatus = "PREPARING"  // 배송 준비 중
	DeliveryStatusShipped    DeliveryStatus = "SHIPPED"    // 배송 중
	DeliveryStatusDelivered  DeliveryStatus = "DELIVERED"  // 배송 완료
	DeliveryStatusCancelled  DeliveryStatus = "CANCELLED"  // 배송 취소
)

// Delivery 배송 엔티티
type Delivery struct {
	ID              int64          `json:"id"`
	OrderID         int64          `json:"order_id"`
	Address         string         `json:"address"`
	Status          DeliveryStatus `json:"status"`
	TrackingNumber  string         `json:"tracking_number"`
	Carrier         string         `json:"carrier"`
	IdempotencyKey  string         `json:"idempotency_key"`
	CreatedAt       time.Time      `json:"created_at"`
	UpdatedAt       time.Time      `json:"updated_at"`
}

// NewDelivery 새로운 배송 생성
func NewDelivery(orderID int64, address, trackingNumber, carrier, idempotencyKey string) *Delivery {
	now := time.Now()
	return &Delivery{
		OrderID:        orderID,
		Address:        address,
		Status:         DeliveryStatusPreparing,
		TrackingNumber: trackingNumber,
		Carrier:        carrier,
		IdempotencyKey: idempotencyKey,
		CreatedAt:      now,
		UpdatedAt:      now,
	}
}

// UpdateStatus 배송 상태 업데이트
func (d *Delivery) UpdateStatus(status DeliveryStatus) {
	d.Status = status
	d.UpdatedAt = time.Now()
}

