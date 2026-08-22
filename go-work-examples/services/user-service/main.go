package main

import (
	"context"
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
	sharederrors "github.com/kyungseok-lee/go-work-examples/shared/errors"
	"github.com/kyungseok-lee/go-work-examples/shared/events"
	"github.com/kyungseok-lee/go-work-examples/shared/types"
	"github.com/kyungseok-lee/go-work-examples/shared/utils"
)

type UserService struct {
	mu    sync.RWMutex
	users map[uuid.UUID]types.User
}

func NewUserService() *UserService {
	return &UserService{
		users: make(map[uuid.UUID]types.User),
	}
}

func (s *UserService) CreateUser(req types.UserCreateRequest) (*types.User, error) {
	if !utils.IsValidEmail(req.Email) {
		return nil, sharederrors.NewValidationErrorWithField("email", "Invalid email format")
	}

	if !utils.IsValidName(req.Name) {
		return nil, sharederrors.NewValidationErrorWithField("name", "Name must be at least 2 characters")
	}

	user := types.User{
		ID:        uuid.New(),
		Email:     req.Email,
		Name:      req.Name,
		CreatedAt: time.Now(),
		UpdatedAt: time.Now(),
	}

	s.mu.Lock()
	s.users[user.ID] = user
	s.mu.Unlock()

	// Publish event
	event := events.NewEvent(events.UserCreatedEvent, events.UserCreatedEventData{
		User: user,
	})
	log.Printf("Event published: %+v", event)

	return &user, nil
}

func (s *UserService) GetUser(id uuid.UUID) (*types.User, error) {
	s.mu.RLock()
	user, exists := s.users[id]
	s.mu.RUnlock()
	if !exists {
		return nil, sharederrors.NewNotFoundErrorWithID(id.String(), "User not found")
	}
	return &user, nil
}

func (s *UserService) UpdateUser(id uuid.UUID, req types.UserUpdateRequest) (*types.User, error) {
	s.mu.Lock()
	defer s.mu.Unlock()

	user, exists := s.users[id]
	if !exists {
		return nil, sharederrors.NewNotFoundErrorWithID(id.String(), "User not found")
	}

	if req.Name != "" {
		if !utils.IsValidName(req.Name) {
			return nil, sharederrors.NewValidationErrorWithField("name", "Name must be at least 2 characters")
		}
		user.Name = req.Name
	}

	user.UpdatedAt = time.Now()
	s.users[id] = user

	return &user, nil
}

func main() {
	userService := NewUserService()

	r := gin.Default()

	r.POST("/users", func(c *gin.Context) {
		var req types.UserCreateRequest
		if err := c.ShouldBindJSON(&req); err != nil {
			c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
			return
		}

		user, err := userService.CreateUser(req)
		if err != nil {
			if httpErr, ok := err.(sharederrors.HTTPError); ok {
				c.JSON(httpErr.HTTPStatus(), gin.H{"error": err.Error()})
			} else {
				c.JSON(http.StatusInternalServerError, gin.H{"error": "Internal server error"})
			}
			return
		}

		c.JSON(http.StatusCreated, user)
	})

	r.GET("/users/:id", func(c *gin.Context) {
		idStr := c.Param("id")
		id, err := uuid.Parse(idStr)
		if err != nil {
			c.JSON(http.StatusBadRequest, gin.H{"error": "Invalid user ID"})
			return
		}

		user, err := userService.GetUser(id)
		if err != nil {
			if httpErr, ok := err.(sharederrors.HTTPError); ok {
				c.JSON(httpErr.HTTPStatus(), gin.H{"error": err.Error()})
			} else {
				c.JSON(http.StatusInternalServerError, gin.H{"error": "Internal server error"})
			}
			return
		}

		c.JSON(http.StatusOK, user)
	})

	r.PUT("/users/:id", func(c *gin.Context) {
		idStr := c.Param("id")
		id, err := uuid.Parse(idStr)
		if err != nil {
			c.JSON(http.StatusBadRequest, gin.H{"error": "Invalid user ID"})
			return
		}

		var req types.UserUpdateRequest
		if err := c.ShouldBindJSON(&req); err != nil {
			c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
			return
		}

		user, err := userService.UpdateUser(id, req)
		if err != nil {
			if httpErr, ok := err.(sharederrors.HTTPError); ok {
				c.JSON(httpErr.HTTPStatus(), gin.H{"error": err.Error()})
			} else {
				c.JSON(http.StatusInternalServerError, gin.H{"error": "Internal server error"})
			}
			return
		}

		c.JSON(http.StatusOK, user)
	})

	// Health check endpoint
	r.GET("/health", func(c *gin.Context) {
		c.JSON(http.StatusOK, gin.H{
			"status":    "healthy",
			"service":   "user-service",
			"timestamp": time.Now().Format(time.RFC3339),
		})
	})

	// Load configuration from environment
	cfg := config.LoadFromEnv()
	if os.Getenv("SERVER_PORT") == "" {
		cfg.Server.Port = "8080"
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
		log.Printf("User service starting on %s", srv.Addr)
		if err := srv.ListenAndServe(); err != nil && err != http.ErrServerClosed {
			log.Fatalf("Failed to start server: %v", err)
		}
	}()

	// Wait for interrupt signal to gracefully shutdown the server
	quit := make(chan os.Signal, 1)
	signal.Notify(quit, syscall.SIGINT, syscall.SIGTERM)
	<-quit
	log.Println("Shutting down user service...")

	// Give outstanding requests 30 seconds to complete
	ctx, cancel := context.WithTimeout(context.Background(), 30*time.Second)
	defer cancel()

	if err := srv.Shutdown(ctx); err != nil {
		log.Fatal("Server forced to shutdown:", err)
	}

	log.Println("User service exited")
}
