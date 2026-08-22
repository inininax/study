package handler

import (
	"context"
	"encoding/json"
	"errors"
	"testing"
	"time"

	commonerrors "github.com/kyungseok/msa-saga-go-examples/common/errors"
	"github.com/kyungseok/msa-saga-go-examples/common/events"
	"github.com/kyungseok/msa-saga-go-examples/common/idempotency"
	"github.com/kyungseok/msa-saga-go-examples/common/messaging"
	"github.com/kyungseok/msa-saga-go-examples/services/order/internal/domain"
	"github.com/kyungseok/msa-saga-go-examples/services/order/internal/service"
	"go.uber.org/zap"
)

// fakeIdemStore 테스트용 멱등성 저장소
type fakeIdemStore struct {
	isProcessedErr    error
	reserveErr        error
	releaseErr        error
	processed         map[string]bool
	reserved          []string
	isProcessedCalled int
}

func newFakeIdemStore() *fakeIdemStore {
	return &fakeIdemStore{processed: make(map[string]bool)}
}

func (f *fakeIdemStore) Reserve(ctx context.Context, key string, ttl time.Duration) (bool, error) {
	if f.reserveErr != nil {
		return false, f.reserveErr
	}
	f.reserved = append(f.reserved, key)
	f.processed[key] = true
	return true, nil
}

func (f *fakeIdemStore) IsProcessed(ctx context.Context, key string) (bool, error) {
	f.isProcessedCalled++
	if f.isProcessedErr != nil {
		return false, f.isProcessedErr
	}
	return f.processed[key], nil
}

func (f *fakeIdemStore) Release(ctx context.Context, key string) error {
	return f.releaseErr
}

// fakeOrderService 테스트용 주문 서비스
type fakeOrderService struct {
	err            error
	calls          []string
	lastPaymentEvt interface{}
}

func (f *fakeOrderService) CreateOrder(ctx context.Context, cmd service.CreateOrderCommand) (*service.CreateOrderResult, error) {
	f.calls = append(f.calls, "CreateOrder")
	return &service.CreateOrderResult{}, f.err
}

func (f *fakeOrderService) GetOrder(ctx context.Context, orderID int64) (*domain.Order, error) {
	f.calls = append(f.calls, "GetOrder")
	return &domain.Order{}, f.err
}

func (f *fakeOrderService) HandlePaymentCompleted(ctx context.Context, evt events.PaymentCompletedEvent) error {
	f.calls = append(f.calls, "HandlePaymentCompleted")
	f.lastPaymentEvt = evt
	return f.err
}

func (f *fakeOrderService) HandlePaymentFailed(ctx context.Context, evt events.PaymentFailedEvent) error {
	f.calls = append(f.calls, "HandlePaymentFailed")
	return f.err
}

func (f *fakeOrderService) HandleStockReserved(ctx context.Context, evt events.StockReservedEvent) error {
	f.calls = append(f.calls, "HandleStockReserved")
	return f.err
}

func (f *fakeOrderService) HandleStockReservationFailed(ctx context.Context, evt events.StockReservationFailedEvent) error {
	f.calls = append(f.calls, "HandleStockReservationFailed")
	return f.err
}

func (f *fakeOrderService) HandleDeliveryStarted(ctx context.Context, evt events.DeliveryStartedEvent) error {
	f.calls = append(f.calls, "HandleDeliveryStarted")
	return f.err
}

func (f *fakeOrderService) HandleDeliveryFailed(ctx context.Context, evt events.DeliveryFailedEvent) error {
	f.calls = append(f.calls, "HandleDeliveryFailed")
	return f.err
}

func newTestHandler(store idempotency.Store, svc *fakeOrderService) *EventHandler {
	return NewEventHandler(svc, store, zap.NewNop())
}

func paymentCompletedMessage(eventID string) *messaging.Message {
	evt := events.PaymentCompletedEvent{
		BaseEvent: events.BaseEvent{
			EventID:       eventID,
			EventType:     events.EventPaymentCompleted,
			SchemaVersion: 1,
			OccurredAt:    time.Now(),
			CorrelationID: "corr-1",
		},
		OrderID: 123,
	}
	data, _ := json.Marshal(evt)
	return &messaging.Message{Topic: string(events.EventPaymentCompleted), Offset: 1, Value: data}
}

func TestEventHandler_SuccessMarksProcessed(t *testing.T) {
	store := newFakeIdemStore()
	svc := &fakeOrderService{}
	h := newTestHandler(store, svc)

	err := h.HandleMessage(context.Background(), paymentCompletedMessage("evt-1"))
	if err != nil {
		t.Fatalf("HandleMessage() error = %v", err)
	}

	if len(svc.calls) != 1 || svc.calls[0] != "HandlePaymentCompleted" {
		t.Errorf("service calls = %v, want [HandlePaymentCompleted]", svc.calls)
	}
	if len(store.reserved) != 1 || store.reserved[0] != "evt-1" {
		t.Errorf("reserved = %v, want [evt-1]", store.reserved)
	}
}

func TestEventHandler_IsProcessedErrorReturnsError(t *testing.T) {
	store := newFakeIdemStore()
	store.isProcessedErr = errors.New("redis down")
	svc := &fakeOrderService{}
	h := newTestHandler(store, svc)

	err := h.HandleMessage(context.Background(), paymentCompletedMessage("evt-1"))
	if err == nil {
		t.Fatal("HandleMessage() should return error when IsProcessed fails")
	}
	if !errors.Is(err, store.isProcessedErr) {
		t.Errorf("error should wrap the underlying IsProcessed failure, got %v", err)
	}
	if len(svc.calls) != 0 {
		t.Errorf("service should not be called, got %v", svc.calls)
	}
	if len(store.reserved) != 0 {
		t.Errorf("nothing should be reserved on failure, got %v", store.reserved)
	}
}

func TestEventHandler_AlreadyProcessedReturnsNil(t *testing.T) {
	store := newFakeIdemStore()
	store.processed["evt-1"] = true
	svc := &fakeOrderService{}
	h := newTestHandler(store, svc)

	err := h.HandleMessage(context.Background(), paymentCompletedMessage("evt-1"))
	if err != nil {
		t.Fatalf("HandleMessage() error = %v", err)
	}
	if len(svc.calls) != 0 {
		t.Errorf("service should not be re-invoked for processed events, got %v", svc.calls)
	}
}

func TestEventHandler_ReserveErrorReturnsError(t *testing.T) {
	store := newFakeIdemStore()
	store.reserveErr = errors.New("redis write failed")
	svc := &fakeOrderService{}
	h := newTestHandler(store, svc)

	err := h.HandleMessage(context.Background(), paymentCompletedMessage("evt-1"))
	if err == nil {
		t.Fatal("HandleMessage() should return error when Reserve fails")
	}
	// 서비스는 호출됐지만 처리 완료 표시가 실패했으므로 재전달 대상이어야 한다
	if len(svc.calls) != 1 {
		t.Errorf("service calls = %v, want exactly one call", svc.calls)
	}
}

func TestEventHandler_ServiceErrorPropagates(t *testing.T) {
	store := newFakeIdemStore()
	svc := &fakeOrderService{err: errors.New("db deadlock")}
	h := newTestHandler(store, svc)

	err := h.HandleMessage(context.Background(), paymentCompletedMessage("evt-1"))
	if err == nil {
		t.Fatal("HandleMessage() should propagate service error")
	}
	if commonerrors.IsBusinessError(err) {
		t.Error("technical service error should not be classified as business error")
	}
	if len(store.reserved) != 0 {
		t.Errorf("failed processing must not mark processed, got %v", store.reserved)
	}
}

func TestEventHandler_MalformedJSONIsMalformedMessage(t *testing.T) {
	store := newFakeIdemStore()
	svc := &fakeOrderService{}
	h := newTestHandler(store, svc)

	msg := &messaging.Message{
		Topic:  string(events.EventPaymentCompleted),
		Offset: 2,
		Value:  []byte(`{"orderId": "not-a-number"`), // 잘린 JSON
	}

	err := h.HandleMessage(context.Background(), msg)
	if err == nil {
		t.Fatal("HandleMessage() should fail on malformed JSON")
	}
	if !commonerrors.IsBusinessError(err) {
		t.Errorf("malformed JSON should be a business error, got %v", err)
	}
	if !commonerrors.IsCode(err, commonerrors.ErrCodeMalformedMessage) {
		t.Errorf("malformed JSON error code = want %s, got %v", commonerrors.ErrCodeMalformedMessage, err)
	}
	if len(svc.calls) != 0 {
		t.Errorf("service should not be called on malformed payload, got %v", svc.calls)
	}
	if len(store.reserved) != 0 {
		t.Errorf("malformed payload must not be marked processed, got %v", store.reserved)
	}
}

func TestEventHandler_UnknownTopicIgnored(t *testing.T) {
	store := newFakeIdemStore()
	svc := &fakeOrderService{}
	h := newTestHandler(store, svc)

	msg := &messaging.Message{Topic: "unknown.topic.v1", Value: []byte("{}")}
	if err := h.HandleMessage(context.Background(), msg); err != nil {
		t.Fatalf("HandleMessage() error = %v", err)
	}
	if len(svc.calls) != 0 || len(store.reserved) != 0 {
		t.Error("unknown topics must be ignored without side effects")
	}
}
