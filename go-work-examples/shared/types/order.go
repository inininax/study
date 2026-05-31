package types

import (
	"time"
	"github.com/google/uuid"
)

type OrderStatus string

const (
	OrderStatusPending   OrderStatus = "pending"
	OrderStatusConfirmed OrderStatus = "confirmed"
	OrderStatusShipped   OrderStatus = "shipped"
	OrderStatusDelivered OrderStatus = "delivered"
	OrderStatusCancelled OrderStatus = "cancelled"
)

type Order struct {
	ID         uuid.UUID   `json:"id"`
	UserID     uuid.UUID   `json:"user_id"`
	Status     OrderStatus `json:"status"`
	TotalPrice float64     `json:"total_price"`
	Items      []OrderItem `json:"items"`
	CreatedAt  time.Time   `json:"created_at"`
	UpdatedAt  time.Time   `json:"updated_at"`
}

type OrderItem struct {
	ID       uuid.UUID `json:"id"`
	Name     string    `json:"name"`
	Price    float64   `json:"price"`
	Quantity int       `json:"quantity"`
}

type OrderCreateRequest struct {
	UserID uuid.UUID          `json:"user_id" validate:"required"`
	Items  []OrderItemRequest `json:"items" validate:"required,min=1"`
}

type OrderItemRequest struct {
	Name     string  `json:"name" validate:"required"`
	Price    float64 `json:"price" validate:"required,gt=0"`
	Quantity int     `json:"quantity" validate:"required,gt=0"`
}