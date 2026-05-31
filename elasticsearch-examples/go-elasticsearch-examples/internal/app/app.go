package app

import (
	"context"
	"os"
	"os/signal"
	"syscall"
	"time"

	"elasticsearch-examples/internal/esclient"
	"elasticsearch-examples/internal/httpapi"
	"elasticsearch-examples/internal/logging"
)

type Config struct {
	ListenAddr     string
	RequestTimeout time.Duration
}

const (
	defaultListenAddr     = ":8080"
	defaultRequestTimeout = 30 * time.Second
	defaultShutdownTimeout = 10 * time.Second
)

// Run은 애플리케이션 전체 라이프사이클을 관리합니다.
// - 설정 로드
// - ES 클라이언트 초기화
// - HTTP 서버 부팅
// - OS 시그널 기반 graceful shutdown
func Run(ctx context.Context) error {
	log := logging.L().With("component", "app")

	cfg := loadConfigFromEnv()

	es, err := esclient.NewFromEnv()
	if err != nil {
		log.Error("failed to create Elasticsearch client", "err", err)
		return err
	}
	// 현재 esclient.Client는 Close가 no-op 이지만, 향후 확장을 위해 남겨둔다.
	defer es.Close()

	srv := httpapi.New(es, cfg.RequestTimeout)
	fiberApp := srv.App()

	log.Info("starting Fiber HTTP server",
		"addr", cfg.ListenAddr,
		"timeout", cfg.RequestTimeout.String(),
	)

	// 서버 시작
	serverErrCh := make(chan error, 1)
	go func() {
		if err := fiberApp.Listen(cfg.ListenAddr); err != nil {
			serverErrCh <- err
		}
	}()

	// 종료 시그널 및 컨텍스트 대기
	sigCh := make(chan os.Signal, 1)
	signal.Notify(sigCh, syscall.SIGINT, syscall.SIGTERM)

	select {
	case <-ctx.Done():
		log.Info("context canceled, shutting down server")
	case sig := <-sigCh:
		log.Info("received termination signal, shutting down server", "signal", sig.String())
	case err := <-serverErrCh:
		log.Error("Fiber server exited with error", "err", err)
		return err
	}

	shutdownCtx, cancel := context.WithTimeout(context.Background(), defaultShutdownTimeout)
	defer cancel()

	if err := fiberApp.ShutdownWithContext(shutdownCtx); err != nil {
		log.Error("error while shutting down Fiber server", "err", err)
		return err
	}

	log.Info("server shutdown completed")
	return nil
}

func loadConfigFromEnv() Config {
	addr := getenv("APP_LISTEN_ADDR", defaultListenAddr)
	timeoutStr := getenv("APP_REQUEST_TIMEOUT", "")

	requestTimeout := defaultRequestTimeout
	if timeoutStr != "" {
		if d, err := time.ParseDuration(timeoutStr); err == nil {
			requestTimeout = d
		} else {
			logging.L().Warn("failed to parse APP_REQUEST_TIMEOUT, using default",
				"value", timeoutStr,
				"default", defaultRequestTimeout.String(),
				"err", err,
			)
		}
	}

	return Config{
		ListenAddr:     addr,
		RequestTimeout: requestTimeout,
	}
}

func getenv(key, def string) string {
	if v := os.Getenv(key); v != "" {
		return v
	}
	return def
}

