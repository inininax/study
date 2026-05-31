package logging

import (
	"log/slog"
	"os"
)

var logger *slog.Logger

func init() {
	level := parseLevel(os.Getenv("LOG_LEVEL"))

	handler := slog.NewJSONHandler(os.Stdout, &slog.HandlerOptions{
		Level: level,
	})

	logger = slog.New(handler)
}

// L는 전역 로거를 반환합니다.
// 운영 환경에서는 JSON 포맷 + 레벨 기반 필터링을 사용합니다.
func L() *slog.Logger {
	return logger
}

func parseLevel(v string) slog.Level {
	switch v {
	case "debug", "DEBUG":
		return slog.LevelDebug
	case "warn", "WARN":
		return slog.LevelWarn
	case "error", "ERROR":
		return slog.LevelError
	default:
		return slog.LevelInfo
	}
}

