package main

import (
	"bytes"
	"encoding/json"
	"fmt"
	"io"
	"net/http"
	"os"
	"time"

	"github.com/google/uuid"
	"github.com/kyungseok-lee/go-work-examples/shared/types"
	"github.com/spf13/cobra"
	"github.com/spf13/viper"
)

var cfgFile string

// httpClient 모든 요청에 타임아웃이 적용된 공유 클라이언트
var httpClient = &http.Client{Timeout: 10 * time.Second}

// rootCmd represents the base command when called without any subcommands
var rootCmd = &cobra.Command{
	Use:   "myapp-cli",
	Short: "CLI tool for MyApp services",
	Long:  `A command line tool to interact with MyApp microservices including user and order management.`,
}

// userCmd represents the user command
var userCmd = &cobra.Command{
	Use:   "user",
	Short: "User management commands",
	Long:  `Commands to manage users in the MyApp platform`,
}

// orderCmd represents the order command
var orderCmd = &cobra.Command{
	Use:   "order",
	Short: "Order management commands",
	Long:  `Commands to manage orders in the MyApp platform`,
}

var createUserCmd = &cobra.Command{
	Use:   "create",
	Short: "Create a new user",
	Long:  `Create a new user with email and name`,
	RunE: func(cmd *cobra.Command, args []string) error {
		email, _ := cmd.Flags().GetString("email")
		name, _ := cmd.Flags().GetString("name")

		if email == "" || name == "" {
			return fmt.Errorf("email and name are required")
		}

		req := types.UserCreateRequest{
			Email: email,
			Name:  name,
		}

		userServiceURL := viper.GetString("services.user")
		return createUser(userServiceURL, req)
	},
}

var getUserCmd = &cobra.Command{
	Use:   "get [user-id]",
	Short: "Get user by ID",
	Long:  `Retrieve user information by user ID`,
	Args:  cobra.ExactArgs(1),
	RunE: func(cmd *cobra.Command, args []string) error {
		userID := args[0]
		userServiceURL := viper.GetString("services.user")
		return getUser(userServiceURL, userID)
	},
}

var createOrderCmd = &cobra.Command{
	Use:   "create",
	Short: "Create a new order",
	Long:  `Create a new order for a user`,
	RunE: func(cmd *cobra.Command, args []string) error {
		userIDStr, _ := cmd.Flags().GetString("user-id")
		itemName, _ := cmd.Flags().GetString("item-name")
		itemPrice, _ := cmd.Flags().GetFloat64("item-price")
		itemQuantity, _ := cmd.Flags().GetInt("item-quantity")

		if userIDStr == "" || itemName == "" || itemPrice <= 0 || itemQuantity <= 0 {
			return fmt.Errorf("user-id, item-name, item-price, and item-quantity are required")
		}

		userID, err := uuid.Parse(userIDStr)
		if err != nil {
			return fmt.Errorf("invalid user ID: %v", err)
		}

		req := types.OrderCreateRequest{
			UserID: userID,
			Items: []types.OrderItemRequest{
				{
					Name:     itemName,
					Price:    itemPrice,
					Quantity: itemQuantity,
				},
			},
		}

		orderServiceURL := viper.GetString("services.order")
		return createOrder(orderServiceURL, req)
	},
}

var getOrderCmd = &cobra.Command{
	Use:   "get [order-id]",
	Short: "Get order by ID",
	Long:  `Retrieve order information by order ID`,
	Args:  cobra.ExactArgs(1),
	RunE: func(cmd *cobra.Command, args []string) error {
		orderID := args[0]
		orderServiceURL := viper.GetString("services.order")
		return getOrder(orderServiceURL, orderID)
	},
}

var updateOrderStatusCmd = &cobra.Command{
	Use:   "update-status [order-id] [status]",
	Short: "Update order status",
	Long:  `Update the status of an order. Valid statuses: pending, confirmed, shipped, delivered, cancelled`,
	Args:  cobra.ExactArgs(2),
	RunE: func(cmd *cobra.Command, args []string) error {
		orderID := args[0]
		status := types.OrderStatus(args[1])

		// Validate status
		validStatuses := []types.OrderStatus{
			types.OrderStatusPending,
			types.OrderStatusConfirmed,
			types.OrderStatusShipped,
			types.OrderStatusDelivered,
			types.OrderStatusCancelled,
		}

		valid := false
		for _, validStatus := range validStatuses {
			if status == validStatus {
				valid = true
				break
			}
		}

		if !valid {
			return fmt.Errorf("invalid status. Valid statuses: pending, confirmed, shipped, delivered, cancelled")
		}

		orderServiceURL := viper.GetString("services.order")
		return updateOrderStatus(orderServiceURL, orderID, status)
	},
}

func doRequest(method, url string, body []byte, wantStatus int) ([]byte, error) {
	var req *http.Request
	var err error
	if body != nil {
		req, err = http.NewRequest(method, url, bytes.NewBuffer(body))
	} else {
		req, err = http.NewRequest(method, url, nil)
	}
	if err != nil {
		return nil, fmt.Errorf("failed to create request: %v", err)
	}
	if body != nil {
		req.Header.Set("Content-Type", "application/json")
	}

	resp, err := httpClient.Do(req)
	if err != nil {
		return nil, err
	}
	defer resp.Body.Close()

	respBody, err := io.ReadAll(resp.Body)
	if err != nil {
		return nil, fmt.Errorf("failed to read response body: %v", err)
	}

	if resp.StatusCode != wantStatus {
		return nil, fmt.Errorf("unexpected status %d: %s", resp.StatusCode, string(respBody))
	}
	return respBody, nil
}

func createUser(baseURL string, req types.UserCreateRequest) error {
	data, err := json.Marshal(req)
	if err != nil {
		return fmt.Errorf("failed to marshal request: %v", err)
	}

	body, err := doRequest(http.MethodPost, baseURL+"/users", data, http.StatusCreated)
	if err != nil {
		return fmt.Errorf("failed to create user: %v", err)
	}
	return printUserCreated(body)
}

func printUserCreated(body []byte) error {
	if len(body) == 0 {
		return fmt.Errorf("empty response")
	}

	var user types.User
	if err := json.Unmarshal(body, &user); err != nil {
		return fmt.Errorf("failed to parse response: %v", err)
	}

	fmt.Printf("User created successfully:\nID: %s\nName: %s\nEmail: %s\nCreated: %s\n",
		user.ID, user.Name, user.Email, user.CreatedAt.Format(time.RFC3339))

	return nil
}

func getUser(baseURL string, userID string) error {
	body, err := doRequest(http.MethodGet, baseURL+"/users/"+userID, nil, http.StatusOK)
	if err != nil {
		return fmt.Errorf("failed to get user: %v", err)
	}

	var user types.User
	if err := json.Unmarshal(body, &user); err != nil {
		return fmt.Errorf("failed to parse response: %v", err)
	}

	fmt.Printf("User Details:\nID: %s\nName: %s\nEmail: %s\nCreated: %s\nUpdated: %s\n",
		user.ID, user.Name, user.Email, user.CreatedAt.Format(time.RFC3339), user.UpdatedAt.Format(time.RFC3339))

	return nil
}

func createOrder(baseURL string, req types.OrderCreateRequest) error {
	data, err := json.Marshal(req)
	if err != nil {
		return fmt.Errorf("failed to marshal request: %v", err)
	}

	body, err := doRequest(http.MethodPost, baseURL+"/orders", data, http.StatusCreated)
	if err != nil {
		return fmt.Errorf("failed to create order: %v", err)
	}

	var order types.Order
	if err := json.Unmarshal(body, &order); err != nil {
		return fmt.Errorf("failed to parse response: %v", err)
	}

	fmt.Printf("Order created successfully:\nID: %s\nUser ID: %s\nStatus: %s\nTotal Price: $%.2f\nItems: %d\nCreated: %s\n",
		order.ID, order.UserID, order.Status, order.TotalPrice, len(order.Items), order.CreatedAt.Format(time.RFC3339))

	return nil
}

func getOrder(baseURL string, orderID string) error {
	body, err := doRequest(http.MethodGet, baseURL+"/orders/"+orderID, nil, http.StatusOK)
	if err != nil {
		return fmt.Errorf("failed to get order: %v", err)
	}

	var order types.Order
	if err := json.Unmarshal(body, &order); err != nil {
		return fmt.Errorf("failed to parse response: %v", err)
	}

	fmt.Printf("Order Details:\nID: %s\nUser ID: %s\nStatus: %s\nTotal Price: $%.2f\nCreated: %s\nUpdated: %s\n\nItems:\n",
		order.ID, order.UserID, order.Status, order.TotalPrice, order.CreatedAt.Format(time.RFC3339), order.UpdatedAt.Format(time.RFC3339))

	for i, item := range order.Items {
		fmt.Printf("  %d. %s - $%.2f x %d = $%.2f\n",
			i+1, item.Name, item.Price, item.Quantity, item.Price*float64(item.Quantity))
	}

	return nil
}

func updateOrderStatus(baseURL string, orderID string, status types.OrderStatus) error {
	reqBody := map[string]interface{}{
		"status": status,
	}
	data, err := json.Marshal(reqBody)
	if err != nil {
		return fmt.Errorf("failed to marshal request: %v", err)
	}

	body, err := doRequest(http.MethodPut, baseURL+"/orders/"+orderID+"/status", data, http.StatusOK)
	if err != nil {
		return fmt.Errorf("failed to update order status: %v", err)
	}

	var order types.Order
	if err := json.Unmarshal(body, &order); err != nil {
		return fmt.Errorf("failed to parse response: %v", err)
	}

	fmt.Printf("Order status updated successfully:\nID: %s\nNew Status: %s\nUpdated: %s\n",
		order.ID, order.Status, order.UpdatedAt.Format(time.RFC3339))

	return nil
}

func initConfig() {
	if cfgFile != "" {
		viper.SetConfigFile(cfgFile)
	} else {
		viper.SetConfigName("config")
		viper.SetConfigType("yaml")
		viper.AddConfigPath(".")
		viper.AddConfigPath("$HOME/.myapp")
		viper.AddConfigPath("/etc/myapp/")
	}

	viper.AutomaticEnv()

	if err := viper.ReadInConfig(); err == nil {
		fmt.Println("Using config file:", viper.ConfigFileUsed())
	}

	// Set default values
	viper.SetDefault("services.user", "http://localhost:8080")
	viper.SetDefault("services.order", "http://localhost:8081")
	viper.SetDefault("services.notification", "http://localhost:8082")
}

func init() {
	cobra.OnInitialize(initConfig)

	rootCmd.PersistentFlags().StringVar(&cfgFile, "config", "", "config file (default is $HOME/.myapp/config.yaml)")

	// User commands
	createUserCmd.Flags().StringP("email", "e", "", "User email address")
	createUserCmd.Flags().StringP("name", "n", "", "User full name")
	createUserCmd.MarkFlagRequired("email")
	createUserCmd.MarkFlagRequired("name")

	userCmd.AddCommand(createUserCmd)
	userCmd.AddCommand(getUserCmd)

	// Order commands
	createOrderCmd.Flags().StringP("user-id", "u", "", "User ID for the order")
	createOrderCmd.Flags().StringP("item-name", "n", "", "Item name")
	createOrderCmd.Flags().Float64P("item-price", "p", 0, "Item price")
	createOrderCmd.Flags().IntP("item-quantity", "q", 1, "Item quantity")
	createOrderCmd.MarkFlagRequired("user-id")
	createOrderCmd.MarkFlagRequired("item-name")
	createOrderCmd.MarkFlagRequired("item-price")
	createOrderCmd.MarkFlagRequired("item-quantity")

	orderCmd.AddCommand(createOrderCmd)
	orderCmd.AddCommand(getOrderCmd)
	orderCmd.AddCommand(updateOrderStatusCmd)

	rootCmd.AddCommand(userCmd)
	rootCmd.AddCommand(orderCmd)
}

func main() {
	if err := rootCmd.Execute(); err != nil {
		fmt.Println(err)
		os.Exit(1)
	}
}
