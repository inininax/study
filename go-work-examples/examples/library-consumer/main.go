package main

import (
	"fmt"
	"log"
	"time"

	"github.com/google/uuid"
	"github.com/kyungseok-lee/go-work-examples/shared/events"
	"github.com/kyungseok-lee/go-work-examples/shared/types"
	"github.com/kyungseok-lee/go-work-examples/shared/utils"
)

// Example demonstrating how to consume the shared library
func main() {
	fmt.Println("=== Go Workspace Library Consumer Example ===")
	fmt.Println()

	// Example 1: Using shared types
	fmt.Println("1. Creating and validating user data:")
	fmt.Println("-----------------------------------")
	
	// Create a user using shared types
	user := types.User{
		ID:        uuid.New(),
		Email:     "demo@example.com",
		Name:      "Demo User",
		CreatedAt: time.Now(),
		UpdatedAt: time.Now(),
	}
	
	fmt.Printf("Created user: %+v\n", user)
	
	// Validate email using shared utilities
	if utils.IsValidEmail(user.Email) {
		fmt.Printf("✓ Email '%s' is valid\n", user.Email)
	} else {
		fmt.Printf("✗ Email '%s' is invalid\n", user.Email)
	}
	
	// Validate name using shared utilities
	if utils.IsValidName(user.Name) {
		fmt.Printf("✓ Name '%s' is valid\n", user.Name)
	} else {
		fmt.Printf("✗ Name '%s' is invalid\n", user.Name)
	}
	
	fmt.Println()

	// Example 2: Working with order types
	fmt.Println("2. Creating order with shared types:")
	fmt.Println("-----------------------------------")
	
	order := types.Order{
		ID:         uuid.New(),
		UserID:     user.ID,
		Status:     types.OrderStatusPending,
		TotalPrice: 299.99,
		Items: []types.OrderItem{
			{
				ID:       uuid.New(),
				Name:     "Wireless Headphones",
				Price:    199.99,
				Quantity: 1,
			},
			{
				ID:       uuid.New(),
				Name:     "Phone Case",
				Price:    29.99,
				Quantity: 1,
			},
			{
				ID:       uuid.New(),
				Name:     "Screen Protector",
				Price:    9.99,
				Quantity: 7,
			},
		},
		CreatedAt: time.Now(),
		UpdatedAt: time.Now(),
	}
	
	fmt.Printf("Created order: ID=%s, Status=%s, Total=$%.2f\n", 
		order.ID.String()[:8]+"...", order.Status, order.TotalPrice)
	
	fmt.Printf("Order items:\n")
	for i, item := range order.Items {
		fmt.Printf("  %d. %s - $%.2f x %d\n", i+1, item.Name, item.Price, item.Quantity)
	}
	
	fmt.Println()

	// Example 3: Event creation and handling
	fmt.Println("3. Working with shared events:")
	fmt.Println("-----------------------------")
	
	// Create user created event
	userCreatedEvent := events.NewEvent(events.UserCreatedEvent, events.UserCreatedEventData{
		User: user,
	})
	
	fmt.Printf("User created event: ID=%s, Type=%s\n", 
		userCreatedEvent.ID.String()[:8]+"...", userCreatedEvent.Type)
	fmt.Printf("Event timestamp: %s\n", userCreatedEvent.Timestamp.Format(time.RFC3339))
	
	// Create order created event
	orderCreatedEvent := events.NewEvent(events.OrderCreatedEvent, events.OrderCreatedEventData{
		Order: order,
		User:  user,
	})
	
	fmt.Printf("Order created event: ID=%s, Type=%s\n", 
		orderCreatedEvent.ID.String()[:8]+"...", orderCreatedEvent.Type)
	
	// Simulate order status update
	oldStatus := order.Status
	order.Status = types.OrderStatusConfirmed
	order.UpdatedAt = time.Now()
	
	orderUpdatedEvent := events.NewEvent(events.OrderUpdatedEvent, events.OrderStatusUpdatedEventData{
		Order:     order,
		OldStatus: oldStatus,
		NewStatus: order.Status,
	})
	
	fmt.Printf("Order updated event: ID=%s, Type=%s\n", 
		orderUpdatedEvent.ID.String()[:8]+"...", orderUpdatedEvent.Type)
	fmt.Printf("Status changed: %s → %s\n", oldStatus, order.Status)
	
	fmt.Println()

	// Example 4: Validation examples
	fmt.Println("4. Validation examples:")
	fmt.Println("----------------------")
	
	testEmails := []string{
		"valid@example.com",
		"invalid-email",
		"test@domain",
		"user@domain.co.uk",
		"",
	}
	
	for _, email := range testEmails {
		status := "✗ INVALID"
		if utils.IsValidEmail(email) {
			status = "✓ VALID"
		}
		fmt.Printf("Email '%s': %s\n", email, status)
	}
	
	fmt.Println()
	
	testNames := []string{
		"John Doe",
		"A",
		"",
		"Alice Smith-Jones",
		"  ",
	}
	
	for _, name := range testNames {
		status := "✗ INVALID"
		if utils.IsValidName(name) {
			status = "✓ VALID"
		}
		fmt.Printf("Name '%s': %s\n", name, status)
	}
	
	fmt.Println()

	// Example 5: Creating request/response structures
	fmt.Println("5. Working with request/response types:")
	fmt.Println("--------------------------------------")
	
	// User creation request
	userCreateReq := types.UserCreateRequest{
		Email: "newuser@example.com",
		Name:  "New User",
	}
	
	fmt.Printf("User create request: %+v\n", userCreateReq)
	
	// Order creation request
	orderCreateReq := types.OrderCreateRequest{
		UserID: user.ID,
		Items: []types.OrderItemRequest{
			{
				Name:     "Gaming Keyboard",
				Price:    89.99,
				Quantity: 1,
			},
			{
				Name:     "Gaming Mouse",
				Price:    59.99,
				Quantity: 1,
			},
		},
	}
	
	fmt.Printf("Order create request: UserID=%s\n", orderCreateReq.UserID.String()[:8]+"...")
	fmt.Printf("Items to order:\n")
	for i, item := range orderCreateReq.Items {
		fmt.Printf("  %d. %s - $%.2f x %d\n", i+1, item.Name, item.Price, item.Quantity)
	}
	
	fmt.Println()

	// Example 6: Demonstrating workspace benefits
	fmt.Println("6. Workspace benefits demonstration:")
	fmt.Println("-----------------------------------")
	fmt.Println("This example demonstrates several key benefits of Go workspaces:")
	fmt.Println("• Shared type definitions across multiple modules")
	fmt.Println("• Common utilities and validation logic")
	fmt.Println("• Event-driven architecture with consistent event types")
	fmt.Println("• Local development with replace directives not needed")
	fmt.Println("• Simplified dependency management across related projects")
	fmt.Println("• Version consistency across all consuming modules")
	
	fmt.Println()
	fmt.Println("=== Example completed successfully! ===")
}

// DemoBusinessLogic shows how shared types can be used in business logic
func DemoBusinessLogic() {
	log.Println("Demonstrating business logic using shared types...")
	
	// This function could contain complex business logic that uses
	// shared types, making it easy to maintain consistency across
	// different services in the workspace
}

// DemoEventProcessing shows event processing patterns
func DemoEventProcessing(event events.Event) error {
	log.Printf("Processing event: %s", event.Type)
	
	switch event.Type {
	case events.UserCreatedEvent:
		log.Println("Handling user created event...")
		// Business logic here
	case events.OrderCreatedEvent:
		log.Println("Handling order created event...")
		// Business logic here
	case events.OrderUpdatedEvent:
		log.Println("Handling order updated event...")
		// Business logic here
	default:
		log.Printf("Unknown event type: %s", event.Type)
	}
	
	return nil
}