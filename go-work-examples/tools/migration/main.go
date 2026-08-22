package main

import (
	"encoding/json"
	"fmt"
	"os"
	"path/filepath"
	"time"

	"github.com/google/uuid"
	"github.com/spf13/cobra"
	"github.com/kyungseok-lee/go-work-examples/shared/types"
)

type Migration struct {
	ID          string    `json:"id"`
	Name        string    `json:"name"`
	Description string    `json:"description"`
	AppliedAt   time.Time `json:"applied_at"`
}

type MigrationManager struct {
	migrationsDir string
	stateFile     string
	appliedMigrations map[string]Migration
}

func NewMigrationManager(migrationsDir, stateFile string) *MigrationManager {
	mm := &MigrationManager{
		migrationsDir:     migrationsDir,
		stateFile:         stateFile,
		appliedMigrations: make(map[string]Migration),
	}
	mm.loadState()
	return mm
}

func (mm *MigrationManager) loadState() {
	data, err := os.ReadFile(mm.stateFile)
	if err != nil {
		return // File doesn't exist yet
	}

	var migrations []Migration
	if err := json.Unmarshal(data, &migrations); err != nil {
		return
	}

	for _, migration := range migrations {
		mm.appliedMigrations[migration.ID] = migration
	}
}

func (mm *MigrationManager) saveState() error {
	var migrations []Migration
	for _, migration := range mm.appliedMigrations {
		migrations = append(migrations, migration)
	}

	data, err := json.MarshalIndent(migrations, "", "  ")
	if err != nil {
		return err
	}

	return os.WriteFile(mm.stateFile, data, 0644)
}

func (mm *MigrationManager) CreateMigration(name, description string) error {
	timestamp := time.Now().Format("20060102150405")
	filename := fmt.Sprintf("%s_%s.json", timestamp, name)
	filepath := filepath.Join(mm.migrationsDir, filename)

	migration := map[string]interface{}{
		"id":          uuid.New().String(),
		"name":        name,
		"description": description,
		"created_at":  time.Now(),
		"operations": []map[string]interface{}{
			{
				"type":        "seed_data",
				"entity":      "example",
				"description": fmt.Sprintf("Sample operation for %s", name),
			},
		},
	}

	data, err := json.MarshalIndent(migration, "", "  ")
	if err != nil {
		return err
	}

	if err := os.MkdirAll(mm.migrationsDir, 0755); err != nil {
		return err
	}

	if err := os.WriteFile(filepath, data, 0644); err != nil {
		return err
	}

	fmt.Printf("Migration created: %s\n", filepath)
	return nil
}

func (mm *MigrationManager) ListMigrations() error {
	files, err := filepath.Glob(filepath.Join(mm.migrationsDir, "*.json"))
	if err != nil {
		return err
	}

	if len(files) == 0 {
		fmt.Println("No migrations found")
		return nil
	}

	fmt.Println("Available migrations:")
	fmt.Println("=====================")

	for _, file := range files {
		data, err := os.ReadFile(file)
		if err != nil {
			continue
		}

		var migration map[string]interface{}
		if err := json.Unmarshal(data, &migration); err != nil {
			continue
		}

		id := migration["id"].(string)
		name := migration["name"].(string)
		description := migration["description"].(string)
		
		status := "PENDING"
		if _, applied := mm.appliedMigrations[id]; applied {
			status = "APPLIED"
		}

		fmt.Printf("ID: %s\n", id)
		fmt.Printf("Name: %s\n", name)
		fmt.Printf("Description: %s\n", description)
		fmt.Printf("Status: %s\n", status)
		if applied := mm.appliedMigrations[id]; applied.AppliedAt != (time.Time{}) {
			fmt.Printf("Applied At: %s\n", applied.AppliedAt.Format(time.RFC3339))
		}
		fmt.Println("---")
	}

	return nil
}

func (mm *MigrationManager) RunMigrations() error {
	files, err := filepath.Glob(filepath.Join(mm.migrationsDir, "*.json"))
	if err != nil {
		return err
	}

	appliedCount := 0
	for _, file := range files {
		data, err := os.ReadFile(file)
		if err != nil {
			return fmt.Errorf("failed to read migration file %s: %v", file, err)
		}

		var migration map[string]interface{}
		if err := json.Unmarshal(data, &migration); err != nil {
			return fmt.Errorf("failed to parse migration file %s: %v", file, err)
		}

		id := migration["id"].(string)
		name := migration["name"].(string)
		description := migration["description"].(string)

		if _, applied := mm.appliedMigrations[id]; applied {
			continue // Skip already applied migrations
		}

		fmt.Printf("Applying migration: %s - %s\n", name, description)

		// Simulate migration execution
		if err := mm.executeMigration(migration); err != nil {
			return fmt.Errorf("failed to execute migration %s: %v", name, err)
		}

		// Record as applied
		mm.appliedMigrations[id] = Migration{
			ID:          id,
			Name:        name,
			Description: description,
			AppliedAt:   time.Now(),
		}

		appliedCount++
		fmt.Printf("✓ Migration applied successfully: %s\n", name)
	}

	if appliedCount == 0 {
		fmt.Println("No new migrations to apply")
	} else {
		fmt.Printf("\nApplied %d migrations successfully\n", appliedCount)
	}

	return mm.saveState()
}

func (mm *MigrationManager) executeMigration(migration map[string]interface{}) error {
	// Simulate different types of migration operations
	operations, ok := migration["operations"].([]interface{})
	if !ok {
		return fmt.Errorf("invalid migration format: missing operations")
	}

	for _, op := range operations {
		operation := op.(map[string]interface{})
		opType := operation["type"].(string)

		switch opType {
		case "seed_data":
			fmt.Printf("  Seeding data for entity: %s\n", operation["entity"])
			time.Sleep(100 * time.Millisecond) // Simulate work
		case "create_schema":
			fmt.Printf("  Creating schema: %s\n", operation["schema"])
			time.Sleep(200 * time.Millisecond)
		case "update_data":
			fmt.Printf("  Updating data: %s\n", operation["description"])
			time.Sleep(150 * time.Millisecond)
		default:
			fmt.Printf("  Executing operation: %s\n", opType)
			time.Sleep(100 * time.Millisecond)
		}
	}

	return nil
}

func (mm *MigrationManager) SeedSampleData() error {
	fmt.Println("Seeding sample data...")
	
	// Simulate seeding users
	sampleUsers := []types.UserCreateRequest{
		{Email: "john@example.com", Name: "John Doe"},
		{Email: "jane@example.com", Name: "Jane Smith"},
		{Email: "admin@example.com", Name: "Admin User"},
	}

	fmt.Println("Creating sample users:")
	for i, user := range sampleUsers {
		fmt.Printf("  %d. %s (%s)\n", i+1, user.Name, user.Email)
	}

	// Simulate seeding orders
	fmt.Println("\nCreating sample orders:")
	sampleOrders := []string{
		"Laptop - $999.99",
		"Smartphone - $699.99",
		"Headphones - $199.99",
	}

	for i, order := range sampleOrders {
		fmt.Printf("  %d. %s\n", i+1, order)
	}

	fmt.Println("\n✓ Sample data seeded successfully")
	return nil
}

var rootCmd = &cobra.Command{
	Use:   "migrate",
	Short: "Database migration tool for MyApp services",
	Long:  `A migration tool to manage database schema changes and data seeding for MyApp microservices.`,
}

var createCmd = &cobra.Command{
	Use:   "create [name]",
	Short: "Create a new migration",
	Long:  `Create a new migration file with the specified name`,
	Args:  cobra.ExactArgs(1),
	RunE: func(cmd *cobra.Command, args []string) error {
		name := args[0]
		description, _ := cmd.Flags().GetString("description")
		migrationsDir, _ := cmd.Flags().GetString("migrations-dir")
		
		if description == "" {
			description = fmt.Sprintf("Migration: %s", name)
		}

		mm := NewMigrationManager(migrationsDir, "migrations_state.json")
		return mm.CreateMigration(name, description)
	},
}

var listCmd = &cobra.Command{
	Use:   "list",
	Short: "List all migrations",
	Long:  `List all available migrations and their status`,
	RunE: func(cmd *cobra.Command, args []string) error {
		migrationsDir, _ := cmd.Flags().GetString("migrations-dir")
		mm := NewMigrationManager(migrationsDir, "migrations_state.json")
		return mm.ListMigrations()
	},
}

var runCmd = &cobra.Command{
	Use:   "up",
	Short: "Run pending migrations",
	Long:  `Execute all pending migrations`,
	RunE: func(cmd *cobra.Command, args []string) error {
		migrationsDir, _ := cmd.Flags().GetString("migrations-dir")
		mm := NewMigrationManager(migrationsDir, "migrations_state.json")
		return mm.RunMigrations()
	},
}

var seedCmd = &cobra.Command{
	Use:   "seed",
	Short: "Seed sample data",
	Long:  `Seed the database with sample data for development and testing`,
	RunE: func(cmd *cobra.Command, args []string) error {
		migrationsDir, _ := cmd.Flags().GetString("migrations-dir")
		mm := NewMigrationManager(migrationsDir, "migrations_state.json")
		return mm.SeedSampleData()
	},
}

func init() {
	rootCmd.PersistentFlags().StringP("migrations-dir", "d", "./migrations", "Directory containing migration files")
	
	createCmd.Flags().StringP("description", "m", "", "Migration description")
	
	rootCmd.AddCommand(createCmd)
	rootCmd.AddCommand(listCmd)
	rootCmd.AddCommand(runCmd)
	rootCmd.AddCommand(seedCmd)
}

func main() {
	if err := rootCmd.Execute(); err != nil {
		fmt.Println(err)
		os.Exit(1)
	}
}