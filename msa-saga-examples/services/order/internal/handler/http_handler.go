package handler

import (
	"encoding/json"
	"errors"
	"net/http"
	"strconv"

	"github.com/google/uuid"
	commonerrors "github.com/kyungseok/msa-saga-go-examples/common/errors"
	"github.com/kyungseok/msa-saga-go-examples/services/order/internal/service"
	"go.uber.org/zap"
)

// HTTPHandler HTTP 핸들러
type HTTPHandler struct {
	orderService service.OrderService
	logger       *zap.Logger
}

// NewHTTPHandler HTTP 핸들러 생성
func NewHTTPHandler(orderService service.OrderService, logger *zap.Logger) *HTTPHandler {
	return &HTTPHandler{
		orderService: orderService,
		logger:       logger,
	}
}

// CreateOrderRequest 주문 생성 요청
type CreateOrderRequest struct {
	UserID         int64  `json:"userId"`
	Amount         int64  `json:"amount"`
	Quantity       int    `json:"quantity"`
	IdempotencyKey string `json:"idempotencyKey,omitempty"`
}

// CreateOrderResponse 주문 생성 응답
type CreateOrderResponse struct {
	OrderID int64  `json:"orderId"`
	Status  string `json:"status"`
}

// ErrorResponse 에러 응답
type ErrorResponse struct {
	Error string `json:"error"`
	Code  string `json:"code,omitempty"`
}

// respondDomainError DomainError 코드를 기준으로 HTTP 상태를 매핑해 응답한다.
// 전체 에러는 서버 로그에만 남기고, 5xx 본문에는 원시 에러 문자열을 노출하지 않는다.
func (h *HTTPHandler) respondDomainError(w http.ResponseWriter, err error) {
	var domainErr *commonerrors.DomainError
	if errors.As(err, &domainErr) {
		switch domainErr.Code {
		case commonerrors.ErrCodeInvalidOrder:
			h.logger.Error("request failed", zap.Error(err))
			h.respondError(w, http.StatusBadRequest, domainErr.Message, string(domainErr.Code))
			return
		case commonerrors.ErrCodeOrderNotFound, commonerrors.ErrCodeNotFound:
			h.logger.Error("request failed", zap.Error(err))
			h.respondError(w, http.StatusNotFound, domainErr.Message, string(domainErr.Code))
			return
		case commonerrors.ErrCodeDuplicateRequest, commonerrors.ErrCodeConflict:
			h.logger.Error("request failed", zap.Error(err))
			h.respondError(w, http.StatusConflict, domainErr.Message, string(domainErr.Code))
			return
		}
	}

	h.logger.Error("request failed with internal error", zap.Error(err))
	h.respondError(w, http.StatusInternalServerError, "internal server error", "")
}

// CreateOrder 주문 생성 API
func (h *HTTPHandler) CreateOrder(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodPost {
		h.respondError(w, http.StatusMethodNotAllowed, "method not allowed", "")
		return
	}

	var req CreateOrderRequest
	if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
		h.respondError(w, http.StatusBadRequest, "invalid request body", "")
		return
	}

	// IdempotencyKey가 없으면 생성
	if req.IdempotencyKey == "" {
		req.IdempotencyKey = uuid.New().String()
	}

	cmd := service.CreateOrderCommand{
		UserID:         req.UserID,
		Amount:         req.Amount,
		Quantity:       req.Quantity,
		IdempotencyKey: req.IdempotencyKey,
	}

	result, err := h.orderService.CreateOrder(r.Context(), cmd)
	if err != nil {
		h.respondDomainError(w, err)
		return
	}

	h.respondJSON(w, http.StatusCreated, CreateOrderResponse{
		OrderID: result.OrderID,
		Status:  string(result.Status),
	})
}

// GetOrder 주문 조회 API
func (h *HTTPHandler) GetOrder(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodGet {
		h.respondError(w, http.StatusMethodNotAllowed, "method not allowed", "")
		return
	}

	// URL에서 orderID 파싱 (예: /orders/123)
	orderIDStr := r.URL.Path[len("/orders/"):]
	orderID, err := strconv.ParseInt(orderIDStr, 10, 64)
	if err != nil {
		h.respondError(w, http.StatusBadRequest, "invalid order ID", "")
		return
	}

	order, err := h.orderService.GetOrder(r.Context(), orderID)
	if err != nil {
		h.respondDomainError(w, err)
		return
	}

	h.respondJSON(w, http.StatusOK, order)
}

// HealthCheck 헬스 체크 API
func (h *HTTPHandler) HealthCheck(w http.ResponseWriter, r *http.Request) {
	h.respondJSON(w, http.StatusOK, map[string]string{"status": "healthy"})
}

func (h *HTTPHandler) respondJSON(w http.ResponseWriter, status int, data interface{}) {
	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(status)
	json.NewEncoder(w).Encode(data)
}

func (h *HTTPHandler) respondError(w http.ResponseWriter, status int, message string, code string) {
	h.respondJSON(w, status, ErrorResponse{
		Error: message,
		Code:  code,
	})
}
