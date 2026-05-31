package main

import (
	"fmt"
	"time"

	"github.com/google/uuid"
	"github.com/kyungseok-lee/go-work-examples/shared/config"
	"github.com/kyungseok-lee/go-work-examples/shared/errors"
	"github.com/kyungseok-lee/go-work-examples/shared/events"
	"github.com/kyungseok-lee/go-work-examples/shared/logger"
	"github.com/kyungseok-lee/go-work-examples/shared/types"
	"github.com/kyungseok-lee/go-work-examples/shared/utils"
)

// WorkspaceDemo demonstrates the power of Go workspaces
func main() {
	fmt.Println("=== Go Workspace Demo ===")
	fmt.Println("This demo shows how Go workspaces enable seamless sharing of code across multiple modules")
	fmt.Println()

	// 1. Configuration Management
	fmt.Println("1. Configuration Management:")
	fmt.Println("----------------------------")
	demoConfig := config.LoadFromEnv()
	fmt.Printf("Server Address: %s\n", demoConfig.GetServerAddress())
	fmt.Printf("Database DSN: %s\n", demoConfig.GetDatabaseDSN())
	fmt.Printf("Environment: %s\n", getEnvironment(demoConfig))
	fmt.Println()

	// 2. Structured Logging
	fmt.Println("2. Structured Logging:")
	fmt.Println("---------------------")
	appLogger := logger.DefaultLogger("workspace-demo")
	appLogger.Info("Application started", map[string]interface{}{
		"version": "1.0.0",
		"env":     getEnvironment(demoConfig),
	})
	appLogger.Debug("Debug message (only visible if LOG_LEVEL=debug)")
	appLogger.Warn("This is a warning message")
	fmt.Println()

	// 3. Shared Types and Validation
	fmt.Println("3. Shared Types and Validation:")
	fmt.Println("-------------------------------")
	demoUser := types.User{
		ID:        uuid.New(),
		Email:     "demo@workspace.example",
		Name:      "Workspace Demo User",
		CreatedAt: time.Now(),
		UpdatedAt: time.Now(),
	}

	fmt.Printf("Created user: %s (%s)\n", demoUser.Name, demoUser.Email)

	// Validate using shared utilities
	if utils.IsValidEmail(demoUser.Email) {
		fmt.Println("✓ Email validation passed")
	}
	if utils.IsValidName(demoUser.Name) {
		fmt.Println("✓ Name validation passed")
	}
	fmt.Println()

	// 4. Error Handling
	fmt.Println("4. Error Handling:")
	fmt.Println("-----------------")

	// Demonstrate different error types
	validationErr := errors.NewValidationErrorWithField("email", "Invalid email format")
	fmt.Printf("Validation Error: %s (HTTP Status: %d)\n", validationErr.Error(), validationErr.HTTPStatus())

	notFoundErr := errors.NewNotFoundErrorWithID("123", "User not found")
	fmt.Printf("Not Found Error: %s (HTTP Status: %d)\n", notFoundErr.Error(), notFoundErr.HTTPStatus())

	conflictErr := errors.NewConflictErrorWithField("email", "Email already exists")
	fmt.Printf("Conflict Error: %s (HTTP Status: %d)\n", conflictErr.Error(), conflictErr.HTTPStatus())
	fmt.Println()

	// 5. Event System
	fmt.Println("5. Event System:")
	fmt.Println("---------------")

	// Create and process events
	userCreatedEvent := events.NewEvent(events.UserCreatedEvent, events.UserCreatedEventData{
		User: demoUser,
	})

	fmt.Printf("Created event: %s\n", userCreatedEvent.Type)
	fmt.Printf("Event ID: %s\n", userCreatedEvent.ID.String()[:8]+"...")
	fmt.Printf("Event timestamp: %s\n", userCreatedEvent.Timestamp.Format(time.RFC3339))

	// Simulate event processing
	processEvent(userCreatedEvent, appLogger)
	fmt.Println()

	// 6. Order Processing Example
	fmt.Println("6. Order Processing Example:")
	fmt.Println("---------------------------")

	order := createSampleOrder(demoUser.ID)
	fmt.Printf("Created order: %s\n", order.ID.String()[:8]+"...")
	fmt.Printf("Total: $%.2f\n", order.TotalPrice)
	fmt.Printf("Items: %d\n", len(order.Items))

	// Create order event
	orderEvent := events.NewEvent(events.OrderCreatedEvent, events.OrderCreatedEventData{
		Order: order,
		User:  demoUser,
	})

	processEvent(orderEvent, appLogger)
	fmt.Println()

	// 7. Workspace Benefits Summary
	fmt.Println("7. Go Workspace Benefits Demonstrated:")
	fmt.Println("--------------------------------------")
	fmt.Println("✓ Shared configuration management across all modules")
	fmt.Println("✓ Consistent logging format and levels")
	fmt.Println("✓ Unified error handling with proper HTTP status codes")
	fmt.Println("✓ Type-safe event system with shared data structures")
	fmt.Println("✓ Common validation utilities")
	fmt.Println("✓ No replace directives needed - direct local module references")
	fmt.Println("✓ Single workspace for all related projects")
	fmt.Println("✓ Consistent dependency versions across all modules")
	fmt.Println("✓ Easy refactoring across the entire codebase")
	fmt.Println()

	appLogger.Info("Demo completed successfully")
	fmt.Println("=== Demo Complete ===")
}

// getEnvironment returns the current environment
func getEnvironment(cfg *config.Config) string {
	if cfg.IsDevelopment() {
		return "development"
	}
	if cfg.IsProduction() {
		return "production"
	}
	return "unknown"
}

// processEvent simulates event processing
func processEvent(event events.Event, logger *logger.Logger) {
	logger.Info("Processing event", map[string]interface{}{
		"event_type": event.Type,
		"event_id":   event.ID.String()[:8] + "...",
	})

	// Simulate processing time
	time.Sleep(100 * time.Millisecond)

	logger.Info("Event processed successfully")
}

// createSampleOrder creates a sample order for demonstration
func createSampleOrder(userID uuid.UUID) types.Order {
	return types.Order{
		ID:     uuid.New(),
		UserID: userID,
		Status: types.OrderStatusPending,
		Items: []types.OrderItem{
			{
				ID:       uuid.New(),
				Name:     "Go Workspace Guide",
				Price:    29.99,
				Quantity: 1,
			},
			{
				ID:       uuid.New(),
				Name:     "Microservices Best Practices",
				Price:    39.99,
				Quantity: 1,
			},
		},
		TotalPrice: 69.98,
		CreatedAt:  time.Now(),
		UpdatedAt:  time.Now(),
	}
}
