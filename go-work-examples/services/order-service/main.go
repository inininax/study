package main

import (
	"context"
	"log"
	"net/http"
	"os"
	"os/signal"
	"syscall"
	"time"

	"github.com/gin-gonic/gin"
	"github.com/google/uuid"
	"github.com/kyungseok-lee/go-work-examples/shared/errors"
	"github.com/kyungseok-lee/go-work-examples/shared/events"
	"github.com/kyungseok-lee/go-work-examples/shared/types"
)

type OrderService struct {
	orders map[uuid.UUID]types.Order
}

func NewOrderService() *OrderService {
	return &OrderService{
		orders: make(map[uuid.UUID]types.Order),
	}
}

func (s *OrderService) CreateOrder(req types.OrderCreateRequest) (*types.Order, error) {
	var items []types.OrderItem
	var totalPrice float64

	for _, itemReq := range req.Items {
		item := types.OrderItem{
			ID:       uuid.New(),
			Name:     itemReq.Name,
			Price:    itemReq.Price,
			Quantity: itemReq.Quantity,
		}
		items = append(items, item)
		totalPrice += itemReq.Price * float64(itemReq.Quantity)
	}

	order := types.Order{
		ID:         uuid.New(),
		UserID:     req.UserID,
		Status:     types.OrderStatusPending,
		TotalPrice: totalPrice,
		Items:      items,
		CreatedAt:  time.Now(),
		UpdatedAt:  time.Now(),
	}

	s.orders[order.ID] = order

	// Publish event
	event := events.NewEvent(events.OrderCreatedEvent, events.OrderCreatedEventData{
		Order: order,
	})
	log.Printf("Event published: %+v", event)

	return &order, nil
}

func (s *OrderService) GetOrder(id uuid.UUID) (*types.Order, error) {
	order, exists := s.orders[id]
	if !exists {
		return nil, errors.NewNotFoundErrorWithID(id.String(), "Order not found")
	}
	return &order, nil
}

func (s *OrderService) UpdateOrderStatus(id uuid.UUID, status types.OrderStatus) (*types.Order, error) {
	order, exists := s.orders[id]
	if !exists {
		return nil, errors.NewNotFoundErrorWithID(id.String(), "Order not found")
	}

	oldStatus := order.Status
	order.Status = status
	order.UpdatedAt = time.Now()
	s.orders[id] = order

	// Publish event
	event := events.NewEvent(events.OrderUpdatedEvent, events.OrderStatusUpdatedEventData{
		Order:     order,
		OldStatus: oldStatus,
		NewStatus: status,
	})
	log.Printf("Event published: %+v", event)

	return &order, nil
}

func (s *OrderService) GetOrdersByUser(userID uuid.UUID) []types.Order {
	var userOrders []types.Order
	for _, order := range s.orders {
		if order.UserID == userID {
			userOrders = append(userOrders, order)
		}
	}
	return userOrders
}

func main() {
	orderService := NewOrderService()

	r := gin.Default()

	r.POST("/orders", func(c *gin.Context) {
		var req types.OrderCreateRequest
		if err := c.ShouldBindJSON(&req); err != nil {
			c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
			return
		}

		order, err := orderService.CreateOrder(req)
		if err != nil {
			c.JSON(http.StatusInternalServerError, gin.H{"error": "Internal server error"})
			return
		}

		c.JSON(http.StatusCreated, order)
	})

	r.GET("/orders/:id", func(c *gin.Context) {
		idStr := c.Param("id")
		id, err := uuid.Parse(idStr)
		if err != nil {
			c.JSON(http.StatusBadRequest, gin.H{"error": "Invalid order ID"})
			return
		}

		order, err := orderService.GetOrder(id)
		if err != nil {
			if httpErr, ok := err.(errors.HTTPError); ok {
				c.JSON(httpErr.HTTPStatus(), gin.H{"error": err.Error()})
			} else {
				c.JSON(http.StatusInternalServerError, gin.H{"error": "Internal server error"})
			}
			return
		}

		c.JSON(http.StatusOK, order)
	})

	r.PUT("/orders/:id/status", func(c *gin.Context) {
		idStr := c.Param("id")
		id, err := uuid.Parse(idStr)
		if err != nil {
			c.JSON(http.StatusBadRequest, gin.H{"error": "Invalid order ID"})
			return
		}

		var req struct {
			Status types.OrderStatus `json:"status" binding:"required"`
		}
		if err := c.ShouldBindJSON(&req); err != nil {
			c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
			return
		}

		order, err := orderService.UpdateOrderStatus(id, req.Status)
		if err != nil {
			if httpErr, ok := err.(errors.HTTPError); ok {
				c.JSON(httpErr.HTTPStatus(), gin.H{"error": err.Error()})
			} else {
				c.JSON(http.StatusInternalServerError, gin.H{"error": "Internal server error"})
			}
			return
		}

		c.JSON(http.StatusOK, order)
	})

	r.GET("/users/:userId/orders", func(c *gin.Context) {
		userIDStr := c.Param("userId")
		userID, err := uuid.Parse(userIDStr)
		if err != nil {
			c.JSON(http.StatusBadRequest, gin.H{"error": "Invalid user ID"})
			return
		}

		orders := orderService.GetOrdersByUser(userID)
		c.JSON(http.StatusOK, orders)
	})

	// Health check endpoint
	r.GET("/health", func(c *gin.Context) {
		c.JSON(http.StatusOK, gin.H{
			"status":    "healthy",
			"service":   "order-service",
			"timestamp": time.Now().Format(time.RFC3339),
		})
	})

	// Create HTTP server
	srv := &http.Server{
		Addr:    ":8081",
		Handler: r,
	}

	// Start server in a goroutine
	go func() {
		log.Println("Order service starting on :8081")
		if err := srv.ListenAndServe(); err != nil && err != http.ErrServerClosed {
			log.Fatalf("Failed to start server: %v", err)
		}
	}()

	// Wait for interrupt signal to gracefully shutdown the server
	quit := make(chan os.Signal, 1)
	signal.Notify(quit, syscall.SIGINT, syscall.SIGTERM)
	<-quit
	log.Println("Shutting down order service...")

	// Give outstanding requests 30 seconds to complete
	ctx, cancel := context.WithTimeout(context.Background(), 30*time.Second)
	defer cancel()

	if err := srv.Shutdown(ctx); err != nil {
		log.Fatal("Server forced to shutdown:", err)
	}

	log.Println("Order service exited")
}
