package errors

import (
	"database/sql"
	"errors"
	"fmt"
	"strings"
	"testing"
)

func TestIsRetryable(t *testing.T) {
	tests := []struct {
		name string
		err  error
		want bool
	}{
		{
			name: "database error is retryable",
			err:  New(ErrCodeDatabaseError, "db down"),
			want: true,
		},
		{
			name: "network error is retryable",
			err:  New(ErrCodeNetworkError, "connection refused"),
			want: true,
		},
		{
			name: "timeout error is retryable",
			err:  New(ErrCodeTimeoutError, "deadline exceeded"),
			want: true,
		},
		{
			name: "wrapped database error is retryable",
			err:  fmt.Errorf("query failed: %w", Wrap(ErrCodeDatabaseError, "exec", errors.New("boom"))),
			want: true,
		},
		{
			name: "business error is not retryable",
			err:  New(ErrCodePaymentDeclined, "declined"),
			want: false,
		},
		{
			name: "malformed message is not retryable",
			err:  New(ErrCodeMalformedMessage, "bad json"),
			want: false,
		},
		{
			name: "plain error is not retryable",
			err:  errors.New("some error"),
			want: false,
		},
		{
			name: "nil error is not retryable",
			err:  nil,
			want: false,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			if got := IsRetryable(tt.err); got != tt.want {
				t.Errorf("IsRetryable() = %v, want %v", got, tt.want)
			}
		})
	}
}

func TestIsBusinessError(t *testing.T) {
	businessCodes := []ErrorCode{
		ErrCodePaymentDeclined,
		ErrCodeOutOfStock,
		ErrCodeInsufficientBalance,
		ErrCodeInvalidOrder,
		ErrCodeOrderNotFound,
		ErrCodeDuplicateRequest,
		ErrCodeNotFound,
		ErrCodeConflict,
		ErrCodeMalformedMessage,
	}

	for _, code := range businessCodes {
		t.Run("business code "+string(code), func(t *testing.T) {
			if got := IsBusinessError(New(code, "test")); !got {
				t.Errorf("IsBusinessError(%s) = false, want true", code)
			}
		})
	}

	tests := []struct {
		name string
		err  error
		want bool
	}{
		{
			name: "wrapped business error via fmt.Errorf",
			err:  fmt.Errorf("handler: %w", New(ErrCodeOutOfStock, "no stock")),
			want: true,
		},
		{
			name: "deeply wrapped business error",
			err:  fmt.Errorf("outer: %w", fmt.Errorf("inner: %w", New(ErrCodeConflict, "conflict"))),
			want: true,
		},
		{
			name: "technical error is not business",
			err:  New(ErrCodeDatabaseError, "db down"),
			want: false,
		},
		{
			name: "serialization error is not business",
			err:  New(ErrCodeSerializationError, "marshal failed"),
			want: false,
		},
		{
			name: "wrapped technical error is not business",
			err:  fmt.Errorf("ctx: %w", New(ErrCodeDatabaseError, "db down")),
			want: false,
		},
		{
			name: "wrapped sql.ErrNoRows defaults to technical, not business",
			err:  fmt.Errorf("payment not found for order: 1: %w", sql.ErrNoRows),
			want: false,
		},
		{
			name: "plain error is not business",
			err:  errors.New("some error"),
			want: false,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			if got := IsBusinessError(tt.err); got != tt.want {
				t.Errorf("IsBusinessError() = %v, want %v", got, tt.want)
			}
		})
	}
}

func TestIsCode(t *testing.T) {
	tests := []struct {
		name string
		err  error
		code ErrorCode
		want bool
	}{
		{
			name: "direct match",
			err:  New(ErrCodeInvalidOrder, "bad order"),
			code: ErrCodeInvalidOrder,
			want: true,
		},
		{
			name: "match through wrapping chain",
			err:  fmt.Errorf("outer: %w", New(ErrCodeOrderNotFound, "missing")),
			code: ErrCodeOrderNotFound,
			want: true,
		},
		{
			name: "different code",
			err:  New(ErrCodeInvalidOrder, "bad order"),
			code: ErrCodeNotFound,
			want: false,
		},
		{
			name: "plain error never matches",
			err:  errors.New("plain"),
			code: ErrCodeInvalidOrder,
			want: false,
		},
		{
			name: "nil error",
			err:  nil,
			code: ErrCodeInvalidOrder,
			want: false,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			if got := IsCode(tt.err, tt.code); got != tt.want {
				t.Errorf("IsCode() = %v, want %v", got, tt.want)
			}
		})
	}
}

func TestWrappedDomainErrorClassification(t *testing.T) {
	// 래핑된 DomainError도 분류 함수가 올바르게 동작해야 한다
	base := Wrap(ErrCodeDatabaseError, "update failed", errors.New("deadlock"))

	wrapped := fmt.Errorf("service layer: %w", base)
	if !IsRetryable(wrapped) {
		t.Error("wrapped DATABASE_ERROR should be retryable")
	}
	if IsBusinessError(wrapped) {
		t.Error("wrapped DATABASE_ERROR should not be business error")
	}
	if !IsCode(wrapped, ErrCodeDatabaseError) {
		t.Error("wrapped error should match its own code")
	}

	// Unwrap 체인을 통해 cause에 접근 가능해야 한다
	var domainErr *DomainError
	if !errors.As(wrapped, &domainErr) {
		t.Fatal("errors.As should find DomainError in chain")
	}
	if domainErr.Cause == nil || domainErr.Cause.Error() != "deadlock" {
		t.Errorf("cause = %v, want deadlock", domainErr.Cause)
	}
}

func TestDomainErrorMessage(t *testing.T) {
	err := New(ErrCodeInvalidOrder, "amount must be positive")
	want := "[INVALID_ORDER] amount must be positive"
	if err.Error() != want {
		t.Errorf("Error() = %q, want %q", err.Error(), want)
	}

	withCause := Wrap(ErrCodeDatabaseError, "query failed", errors.New("timeout"))
	got := withCause.Error()
	if !strings.Contains(got, "[DATABASE_ERROR]") || !strings.Contains(got, "query failed") || !strings.Contains(got, "timeout") {
		t.Errorf("Error() = %q, want it to contain code, message and cause", got)
	}
}
