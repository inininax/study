package main

import (
	"context"
	"database/sql"
	"encoding/json"
	"fmt"
	"net/http"
	"os"
	"os/signal"
	"strings"
	"syscall"
	"time"

	_ "github.com/lib/pq"
	"github.com/redis/go-redis/v9"
	"go.uber.org/zap"

	commonerrors "github.com/kyungseok/msa-saga-go-examples/common/errors"
	"github.com/kyungseok/msa-saga-go-examples/common/events"
	"github.com/kyungseok/msa-saga-go-examples/common/idempotency"
	"github.com/kyungseok/msa-saga-go-examples/common/logger"
	"github.com/kyungseok/msa-saga-go-examples/common/messaging"
	"github.com/kyungseok/msa-saga-go-examples/services/delivery/internal/repository"
	"github.com/kyungseok/msa-saga-go-examples/services/delivery/internal/service"
	"github.com/kyungseok/msa-saga-go-examples/services/delivery/internal/worker"
)

func main() {
	// 전체 라이프사이클 컨텍스트 (컨슈머/워커 종료 신호로 사용)
	ctx, cancel := context.WithCancel(context.Background())
	defer cancel()

	log, _ := logger.NewLogger("delivery-service", true)
	defer log.Sync()

	config := loadConfig()

	db, err := sql.Open("postgres", config.DBDSN)
	if err != nil {
		log.Fatal("failed to connect to database", zap.Error(err))
	}
	defer db.Close()

	db.SetMaxOpenConns(25)
	db.SetMaxIdleConns(10)
	db.SetConnMaxLifetime(5 * time.Minute)

	if err := db.Ping(); err != nil {
		log.Fatal("failed to ping database", zap.Error(err))
	}
	log.Info("connected to database")

	redisClient := redis.NewClient(&redis.Options{Addr: config.RedisAddr})
	defer redisClient.Close()

	publisher, err := messaging.NewKafkaPublisher(config.KafkaBrokers, log)
	if err != nil {
		log.Fatal("failed to create kafka publisher", zap.Error(err))
	}
	defer publisher.Close()

	// Repository 생성
	deliveryRepo := repository.NewDeliveryRepository(db)
	outboxRepo := repository.NewOutboxRepository(db)

	// Service 생성
	deliveryService := service.NewDeliveryService(deliveryRepo, outboxRepo, log)
	idemStore := idempotency.NewRedisStore(redisClient, "delivery-service")

	consumer, err := messaging.NewKafkaConsumer(config.KafkaBrokers, "delivery-service-group", log)
	if err != nil {
		log.Fatal("failed to create kafka consumer", zap.Error(err))
	}
	defer consumer.Close()

	topics := []string{"stock.reserved.v1"}

	// Event Handler (fail-closed 멱등성: 조회/예약 실패 시 에러 반환 → 재전달)
	eventHandler := func(ctx context.Context, msg *messaging.Message) error {
		log.Info("received message", zap.String("topic", msg.Topic))

		var evt events.StockReservedEvent
		if err := json.Unmarshal(msg.Value, &evt); err != nil {
			log.Error("malformed message payload", zap.String("topic", msg.Topic), zap.Error(err))
			return commonerrors.Wrap(commonerrors.ErrCodeMalformedMessage, "failed to unmarshal event payload", err)
		}

		processed, err := idemStore.IsProcessed(ctx, evt.EventID)
		if err != nil {
			log.Error("idempotency check failed", zap.String("eventId", evt.EventID), zap.Error(err))
			return fmt.Errorf("idempotency check failed for event %s: %w", evt.EventID, err)
		}
		if processed {
			return nil
		}

		if err := deliveryService.HandleStockReserved(ctx, evt); err != nil {
			return err
		}

		if _, err := idemStore.Reserve(ctx, evt.EventID, 24*time.Hour); err != nil {
			log.Error("failed to mark event processed", zap.String("eventId", evt.EventID), zap.Error(err))
			return fmt.Errorf("failed to mark event %s processed: %w", evt.EventID, err)
		}
		return nil
	}

	if err := consumer.Subscribe(ctx, topics, eventHandler); err != nil {
		log.Fatal("failed to subscribe", zap.Error(err))
	}
	log.Info("subscribed to kafka topics", zap.Strings("topics", topics))

	outboxWorker := worker.NewOutboxWorker(outboxRepo, publisher, log, 1*time.Second)
	go outboxWorker.Start(ctx)

	// HTTP Server
	mux := http.NewServeMux()
	mux.HandleFunc("/health", func(w http.ResponseWriter, r *http.Request) {
		w.WriteHeader(http.StatusOK)
		w.Write([]byte(`{"status":"healthy"}`))
	})

	server := &http.Server{Addr: ":" + config.ServicePort, Handler: mux}

	go func() {
		log.Info("http server starting", zap.String("port", config.ServicePort))
		if err := server.ListenAndServe(); err != nil && err != http.ErrServerClosed {
			log.Fatal("http server failed", zap.Error(err))
		}
	}()

	quit := make(chan os.Signal, 1)
	signal.Notify(quit, syscall.SIGINT, syscall.SIGTERM)
	<-quit

	log.Info("shutting down server...")
	shutdownCtx, shutdownCancel := context.WithTimeout(context.Background(), 10*time.Second)
	defer shutdownCancel()

	if err := server.Shutdown(shutdownCtx); err != nil {
		log.Error("server forced to shutdown", zap.Error(err))
	}

	cancel() // 컨슈머 루프와 outbox worker 종료
	log.Info("server stopped")
}

type Config struct {
	DBDSN        string
	RedisAddr    string
	KafkaBrokers []string
	ServicePort  string
}

func loadConfig() Config {
	return Config{
		DBDSN:        getEnv("DB_DSN", "postgres://delivery:delivery@localhost:54324/delivery_db?sslmode=disable"),
		RedisAddr:    getEnv("REDIS_ADDR", "localhost:6379"),
		KafkaBrokers: strings.Split(getEnv("KAFKA_BROKERS", "localhost:9093"), ","),
		ServicePort:  getEnv("SERVICE_PORT", "8004"),
	}
}

func getEnv(key, defaultValue string) string {
	if value := os.Getenv(key); value != "" {
		return value
	}
	return defaultValue
}
