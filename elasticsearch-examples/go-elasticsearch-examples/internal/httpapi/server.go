package httpapi

import (
	"context"
	"time"

	"elasticsearch-examples/internal/esclient"
	"elasticsearch-examples/internal/scenario"

	"github.com/gofiber/fiber/v2"
)

type Server struct {
	app            *fiber.App
	es             *esclient.Client
	requestTimeout time.Duration
}

func New(es *esclient.Client, requestTimeout time.Duration) *Server {
	app := fiber.New(fiber.Config{
		AppName: "Elasticsearch Examples (Fiber)",
	})

	s := &Server{
		app:            app,
		es:             es,
		requestTimeout: requestTimeout,
	}

	s.registerRoutes()
	return s
}

func (s *Server) App() *fiber.App {
	return s.app
}

func (s *Server) registerRoutes() {
	s.app.Get("/health", s.handleHealth)

	api := s.app.Group("/api")
	api.Post("/scenarios/:name", s.handleRunScenario)
}

func (s *Server) handleHealth(c *fiber.Ctx) error {
	ctx, cancel := context.WithTimeout(c.UserContext(), 5*time.Second)
	defer cancel()

	if err := s.es.HealthCheck(ctx); err != nil {
		return c.Status(fiber.StatusServiceUnavailable).JSON(fiber.Map{
			"status":  "unhealthy",
			"message": err.Error(),
		})
	}

	return c.JSON(fiber.Map{
		"status": "ok",
	})
}

type runScenarioRequest struct {
	Reset bool `json:"reset"`
}

func (s *Server) handleRunScenario(c *fiber.Ctx) error {
	name := c.Params("name")

	var body runScenarioRequest
	if err := c.BodyParser(&body); err != nil && len(c.Body()) > 0 {
		return c.Status(fiber.StatusBadRequest).JSON(fiber.Map{
			"error":   "invalid request body",
			"details": err.Error(),
		})
	}

	handler, ok := scenarioHandler(name)
	if !ok {
		return c.Status(fiber.StatusNotFound).JSON(fiber.Map{
			"error":   "unknown scenario",
			"details": name,
		})
	}

	ctx, cancel := context.WithTimeout(c.UserContext(), s.requestTimeout)
	defer cancel()

	if err := handler(ctx, s.es, body.Reset); err != nil {
		return c.Status(fiber.StatusInternalServerError).JSON(fiber.Map{
			"error":   "scenario execution failed",
			"details": err.Error(),
		})
	}

	return c.JSON(fiber.Map{
		"scenario": name,
		"reset":    body.Reset,
		"status":   "ok",
	})
}

type scenarioHandlerFunc func(ctx context.Context, c *esclient.Client, reset bool) error

func scenarioHandler(name string) (scenarioHandlerFunc, bool) {
	switch name {
	case "product-search":
		return scenario.RunProductSearchScenario, true
	case "log-analytics":
		return scenario.RunLogAnalyticsScenario, true
	case "autocomplete":
		return scenario.RunAutocompleteScenario, true
	case "advanced-indexing":
		return scenario.RunAdvancedIndexingScenario, true
	default:
		return nil, false
	}
}

