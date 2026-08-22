package domain

import "testing"

func TestOrder_CanTransitionTo(t *testing.T) {
	tests := []struct {
		name    string
		current OrderStatus
		next    OrderStatus
		want    bool
	}{
		// 정상 진행 경로
		{name: "PENDING to PAYMENT_PROCESSING", current: OrderStatusPending, next: OrderStatusPaymentProcessing, want: true},
		{name: "PENDING to STOCK_RESERVING (결제 완료 후 바로 예약 단계)", current: OrderStatusPending, next: OrderStatusStockReserving, want: true},
		{name: "PAYMENT_PROCESSING to STOCK_RESERVING", current: OrderStatusPaymentProcessing, next: OrderStatusStockReserving, want: true},
		{name: "STOCK_RESERVING to DELIVERY_PREPARING", current: OrderStatusStockReserving, next: OrderStatusDeliveryPreparing, want: true},
		{name: "DELIVERY_PREPARING to COMPLETED", current: OrderStatusDeliveryPreparing, next: OrderStatusCompleted, want: true},

		// 취소/실패 경로
		{name: "PENDING to CANCELED", current: OrderStatusPending, next: OrderStatusCanceled, want: true},
		{name: "STOCK_RESERVING to CANCELED", current: OrderStatusStockReserving, next: OrderStatusCanceled, want: true},
		{name: "DELIVERY_PREPARING to FAILED", current: OrderStatusDeliveryPreparing, next: OrderStatusFailed, want: true},

		// 불가능한 전이 (역방향/건너뛰기)
		{name: "PENDING skips to DELIVERY_PREPARING", current: OrderStatusPending, next: OrderStatusDeliveryPreparing, want: false},
		{name: "PENDING skips to COMPLETED", current: OrderStatusPending, next: OrderStatusCompleted, want: false},
		{name: "STOCK_RESERVING back to PENDING", current: OrderStatusStockReserving, next: OrderStatusPending, want: false},
		{name: "DELIVERY_PREPARING back to STOCK_RESERVING", current: OrderStatusDeliveryPreparing, next: OrderStatusStockReserving, want: false},

		// 종결 상태는 어떤 전이도 불가
		{name: "COMPLETED rejects CANCELED", current: OrderStatusCompleted, next: OrderStatusCanceled, want: false},
		{name: "COMPLETED rejects FAILED", current: OrderStatusCompleted, next: OrderStatusFailed, want: false},
		{name: "COMPLETED rejects COMPLETED", current: OrderStatusCompleted, next: OrderStatusCompleted, want: false},
		{name: "CANCELED rejects COMPLETED", current: OrderStatusCanceled, next: OrderStatusCompleted, want: false},
		{name: "CANCELED rejects PENDING", current: OrderStatusCanceled, next: OrderStatusPending, want: false},
		{name: "FAILED rejects COMPLETED", current: OrderStatusFailed, next: OrderStatusCompleted, want: false},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			o := &Order{ID: 1, Status: tt.current}
			if got := o.CanTransitionTo(tt.next); got != tt.want {
				t.Errorf("CanTransitionTo(%s -> %s) = %v, want %v", tt.current, tt.next, got, tt.want)
			}
		})
	}
}

func TestOrder_TransitionTo(t *testing.T) {
	t.Run("legal transition updates status and version-independent fields", func(t *testing.T) {
		o := &Order{ID: 1, Status: OrderStatusPending}
		if !o.TransitionTo(OrderStatusStockReserving) {
			t.Fatal("TransitionTo should succeed for legal transition")
		}
		if o.Status != OrderStatusStockReserving {
			t.Errorf("status = %s, want %s", o.Status, OrderStatusStockReserving)
		}
		if o.UpdatedAt.IsZero() {
			t.Error("UpdatedAt should be set after transition")
		}
	})

	t.Run("illegal transition leaves order unchanged", func(t *testing.T) {
		o := &Order{ID: 1, Status: OrderStatusCompleted}
		if o.TransitionTo(OrderStatusCanceled) {
			t.Fatal("TransitionTo should fail when COMPLETED -> CANCELED")
		}
		if o.Status != OrderStatusCompleted {
			t.Errorf("status = %s, want %s", o.Status, OrderStatusCompleted)
		}
	})
}
