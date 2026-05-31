package events

import (
	"time"
	"github.com/google/uuid"
	"github.com/kyungseok-lee/go-work-examples/shared/types"
)

type EventType string

const (
	UserCreatedEvent    EventType = "user.created"
	UserUpdatedEvent    EventType = "user.updated"
	OrderCreatedEvent   EventType = "order.created"
	OrderUpdatedEvent   EventType = "order.updated"
	OrderShippedEvent   EventType = "order.shipped"
	OrderDeliveredEvent EventType = "order.delivered"
)

type Event struct {
	ID        uuid.UUID   `json:"id"`
	Type      EventType   `json:"type"`
	Data      interface{} `json:"data"`
	Timestamp time.Time   `json:"timestamp"`
}

type UserCreatedEventData struct {
	User types.User `json:"user"`
}

type OrderCreatedEventData struct {
	Order types.Order `json:"order"`
	User  types.User  `json:"user"`
}

type OrderStatusUpdatedEventData struct {
	Order     types.Order       `json:"order"`
	OldStatus types.OrderStatus `json:"old_status"`
	NewStatus types.OrderStatus `json:"new_status"`
}

func NewEvent(eventType EventType, data interface{}) Event {
	return Event{
		ID:        uuid.New(),
		Type:      eventType,
		Data:      data,
		Timestamp: time.Now(),
	}
}