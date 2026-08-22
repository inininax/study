package main

import (
	"context"
	"encoding/json"
	"fmt"
	"log"
	"net/http"
	"os"
	"os/signal"
	"sync"
	"syscall"
	"time"

	"github.com/gin-gonic/gin"
	"github.com/google/uuid"
	"github.com/kyungseok-lee/go-work-examples/shared/config"
	"github.com/kyungseok-lee/go-work-examples/shared/events"
	"github.com/kyungseok-lee/go-work-examples/shared/types"
)

type NotificationType string

const (
	EmailNotification NotificationType = "email"
	SMSNotification   NotificationType = "sms"
	PushNotification  NotificationType = "push"
)

type Notification struct {
	ID        uuid.UUID        `json:"id"`
	UserID    uuid.UUID        `json:"user_id"`
	Type      NotificationType `json:"type"`
	Subject   string           `json:"subject"`
	Message   string           `json:"message"`
	Status    string           `json:"status"`
	CreatedAt time.Time        `json:"created_at"`
	SentAt    *time.Time       `json:"sent_at,omitempty"`
}

type NotificationService struct {
	mu            sync.RWMutex
	notifications map[uuid.UUID]Notification
}

func NewNotificationService() *NotificationService {
	return &NotificationService{
		notifications: make(map[uuid.UUID]Notification),
	}
}

func (s *NotificationService) ProcessEvent(event events.Event) error {
	switch event.Type {
	case events.UserCreatedEvent:
		return s.handleUserCreated(event)
	case events.OrderCreatedEvent:
		return s.handleOrderCreated(event)
	case events.OrderUpdatedEvent:
		return s.handleOrderUpdated(event)
	default:
		log.Printf("Unknown event type: %s", event.Type)
	}
	return nil
}

func (s *NotificationService) handleUserCreated(event events.Event) error {
	dataBytes, err := json.Marshal(event.Data)
	if err != nil {
		return fmt.Errorf("failed to marshal event data: %w", err)
	}
	var eventData events.UserCreatedEventData
	if err := json.Unmarshal(dataBytes, &eventData); err != nil {
		return err
	}

	notification := Notification{
		ID:        uuid.New(),
		UserID:    eventData.User.ID,
		Type:      EmailNotification,
		Subject:   "Welcome!",
		Message:   fmt.Sprintf("Welcome to our platform, %s!", eventData.User.Name),
		Status:    "pending",
		CreatedAt: time.Now(),
	}

	s.mu.Lock()
	s.notifications[notification.ID] = notification
	s.mu.Unlock()
	log.Printf("Created welcome notification for user: %s", eventData.User.Name)

	// Simulate sending notification
	go s.sendNotification(notification.ID)

	return nil
}

func (s *NotificationService) handleOrderCreated(event events.Event) error {
	dataBytes, err := json.Marshal(event.Data)
	if err != nil {
		return fmt.Errorf("failed to marshal event data: %w", err)
	}
	var eventData events.OrderCreatedEventData
	if err := json.Unmarshal(dataBytes, &eventData); err != nil {
		return err
	}

	notification := Notification{
		ID:      uuid.New(),
		UserID:  eventData.Order.UserID,
		Type:    EmailNotification,
		Subject: "Order Confirmation",
		Message: fmt.Sprintf("Your order #%s has been confirmed. Total: $%.2f",
			eventData.Order.ID.String()[:8], eventData.Order.TotalPrice),
		Status:    "pending",
		CreatedAt: time.Now(),
	}

	s.mu.Lock()
	s.notifications[notification.ID] = notification
	s.mu.Unlock()
	log.Printf("Created order confirmation notification for order: %s", eventData.Order.ID)

	// Simulate sending notification
	go s.sendNotification(notification.ID)

	return nil
}

func (s *NotificationService) handleOrderUpdated(event events.Event) error {
	dataBytes, err := json.Marshal(event.Data)
	if err != nil {
		return fmt.Errorf("failed to marshal event data: %w", err)
	}
	var eventData events.OrderStatusUpdatedEventData
	if err := json.Unmarshal(dataBytes, &eventData); err != nil {
		return err
	}

	var subject, message string
	switch eventData.NewStatus {
	case types.OrderStatusShipped:
		subject = "Order Shipped"
		message = fmt.Sprintf("Your order #%s has been shipped!", eventData.Order.ID.String()[:8])
	case types.OrderStatusDelivered:
		subject = "Order Delivered"
		message = fmt.Sprintf("Your order #%s has been delivered!", eventData.Order.ID.String()[:8])
	case types.OrderStatusCancelled:
		subject = "Order Cancelled"
		message = fmt.Sprintf("Your order #%s has been cancelled.", eventData.Order.ID.String()[:8])
	default:
		return nil // Don't send notification for other status changes
	}

	notification := Notification{
		ID:        uuid.New(),
		UserID:    eventData.Order.UserID,
		Type:      EmailNotification,
		Subject:   subject,
		Message:   message,
		Status:    "pending",
		CreatedAt: time.Now(),
	}

	s.mu.Lock()
	s.notifications[notification.ID] = notification
	s.mu.Unlock()
	log.Printf("Created order status notification for order: %s", eventData.Order.ID)

	// Simulate sending notification
	go s.sendNotification(notification.ID)

	return nil
}

func (s *NotificationService) sendNotification(notificationID uuid.UUID) {
	// Simulate processing time
	time.Sleep(2 * time.Second)

	s.mu.Lock()
	defer s.mu.Unlock()

	notification, exists := s.notifications[notificationID]
	if !exists {
		return
	}

	// Simulate sending logic
	log.Printf("Sending %s notification: %s", notification.Type, notification.Subject)

	// Update notification status
	now := time.Now()
	notification.Status = "sent"
	notification.SentAt = &now
	s.notifications[notificationID] = notification

	log.Printf("Notification sent successfully: %s", notification.ID)
}

func (s *NotificationService) GetNotificationsByUser(userID uuid.UUID) []Notification {
	s.mu.RLock()
	defer s.mu.RUnlock()

	var userNotifications []Notification
	for _, notification := range s.notifications {
		if notification.UserID == userID {
			userNotifications = append(userNotifications, notification)
		}
	}
	return userNotifications
}

func main() {
	notificationService := NewNotificationService()

	r := gin.Default()

	// Webhook endpoint to receive events from other services
	r.POST("/webhook/events", func(c *gin.Context) {
		var event events.Event
		if err := c.ShouldBindJSON(&event); err != nil {
			c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
			return
		}

		if err := notificationService.ProcessEvent(event); err != nil {
			c.JSON(http.StatusInternalServerError, gin.H{"error": "Failed to process event"})
			return
		}

		c.JSON(http.StatusOK, gin.H{"message": "Event processed"})
	})

	// Get notifications for a user
	r.GET("/users/:userId/notifications", func(c *gin.Context) {
		userIDStr := c.Param("userId")
		userID, err := uuid.Parse(userIDStr)
		if err != nil {
			c.JSON(http.StatusBadRequest, gin.H{"error": "Invalid user ID"})
			return
		}

		notifications := notificationService.GetNotificationsByUser(userID)
		c.JSON(http.StatusOK, notifications)
	})

	// Health check endpoint
	r.GET("/health", func(c *gin.Context) {
		c.JSON(http.StatusOK, gin.H{"status": "healthy"})
	})

	// Load configuration from environment
	cfg := config.LoadFromEnv()
	if os.Getenv("SERVER_PORT") == "" {
		cfg.Server.Port = "8082"
	}

	// Create HTTP server
	srv := &http.Server{
		Addr:              cfg.GetServerAddress(),
		Handler:           r,
		ReadHeaderTimeout: 5 * time.Second,
		ReadTimeout:       time.Duration(cfg.Server.ReadTimeout) * time.Second,
		WriteTimeout:      time.Duration(cfg.Server.WriteTimeout) * time.Second,
		IdleTimeout:       60 * time.Second,
	}

	// Start server in a goroutine
	go func() {
		log.Printf("Notification service starting on %s", srv.Addr)
		if err := srv.ListenAndServe(); err != nil && err != http.ErrServerClosed {
			log.Fatalf("Failed to start server: %v", err)
		}
	}()

	// Wait for interrupt signal to gracefully shutdown the server
	quit := make(chan os.Signal, 1)
	signal.Notify(quit, syscall.SIGINT, syscall.SIGTERM)
	<-quit
	log.Println("Shutting down notification service...")

	// Give outstanding requests 30 seconds to complete
	ctx, cancel := context.WithTimeout(context.Background(), 30*time.Second)
	defer cancel()

	if err := srv.Shutdown(ctx); err != nil {
		log.Fatal("Server forced to shutdown:", err)
	}

	log.Println("Notification service exited")
}
