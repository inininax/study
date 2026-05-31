package main

import (
	"encoding/json"
	"fmt"
	"io"
	"log"
	"net"
	"os"
	"path/filepath"
	"time"

	"github.com/gofiber/fiber/v2"
	"github.com/gofiber/fiber/v2/middleware/cors"
	"github.com/gofiber/fiber/v2/middleware/logger"
	"github.com/sirupsen/logrus"
)

type LogEntry struct {
	Timestamp string                 `json:"timestamp"`
	Level     string                 `json:"level"`
	Message   string                 `json:"message"`
	Service   string                 `json:"service"`
	Fields    map[string]interface{} `json:"fields"`
}

type LogRequest struct {
	Message string                 `json:"message"`
	Level   string                 `json:"level"`
	Fields  map[string]interface{} `json:"fields"`
}

var (
	logstashConn net.Conn
	fileLogger   *logrus.Logger
)

func main() {
	// 로그 디렉토리 생성
	logDir := "/var/log/app"
	if err := os.MkdirAll(logDir, 0755); err != nil {
		log.Printf("로그 디렉토리 생성 실패: %v", err)
	}

	// 파일 로거 설정
	fileLogger = setupFileLogger(logDir)

	// Logstash 연결 설정
	logstashHost := getEnv("LOGSTASH_HOST", "localhost")
	logstashPort := getEnv("LOGSTASH_PORT", "5000")

	// Logstash TCP 연결
	conn, err := net.Dial("tcp", fmt.Sprintf("%s:%s", logstashHost, logstashPort))
	if err != nil {
		log.Printf("Logstash 연결 실패: %v", err)
	} else {
		logstashConn = conn
		defer conn.Close()
	}

	// Fiber 앱 생성
	app := fiber.New(fiber.Config{
		AppName:      "ELK Example Server",
		ServerHeader: "ELK-Example-Server",
		AppVersion:   "1.0.0",
	})

	// 미들웨어 설정
	app.Use(cors.New())
	app.Use(logger.New())

	// 라우트 설정
	app.Get("/", func(c *fiber.Ctx) error {
		sendLog("info", "Health check endpoint accessed", map[string]interface{}{
			"endpoint": "/",
			"method":   "GET",
		})
		return c.JSON(fiber.Map{
			"message": "ELK Example Server is running",
			"version": "1.0.0",
			"time":    time.Now().Format(time.RFC3339),
			"github":  "https://github.com/kyungseok-lee/elk-examples",
		})
	})

	app.Get("/logs", func(c *fiber.Ctx) error {
		sendLog("info", "Logs endpoint accessed", map[string]interface{}{
			"endpoint": "/logs",
			"method":   "GET",
		})
		return c.JSON(fiber.Map{
			"logs": []LogEntry{
				{
					Timestamp: time.Now().Format(time.RFC3339),
					Level:     "info",
					Message:   "Sample log entry 1",
					Service:   "go-server",
					Fields:    map[string]interface{}{"user_id": 123, "action": "view"},
				},
				{
					Timestamp: time.Now().Add(-1 * time.Minute).Format(time.RFC3339),
					Level:     "warn",
					Message:   "Sample warning log",
					Service:   "go-server",
					Fields:    map[string]interface{}{"user_id": 456, "action": "login_failed"},
				},
				{
					Timestamp: time.Now().Add(-2 * time.Minute).Format(time.RFC3339),
					Level:     "error",
					Message:   "Sample error log",
					Service:   "go-server",
					Fields:    map[string]interface{}{"user_id": 789, "action": "payment_failed", "error_code": "INSUFFICIENT_FUNDS"},
				},
			},
		})
	})

	app.Post("/logs", func(c *fiber.Ctx) error {
		var req LogRequest
		if err := c.BodyParser(&req); err != nil {
			sendLog("error", "Failed to parse log request", map[string]interface{}{
				"error": err.Error(),
			})
			return c.Status(400).JSON(fiber.Map{"error": "Invalid request body"})
		}

		// Logstash로 로그 전송
		sendLog(req.Level, req.Message, req.Fields)

		return c.JSON(fiber.Map{
			"message":   "Log sent successfully",
			"timestamp": time.Now().Format(time.RFC3339),
		})
	})

	app.Get("/generate-logs", func(c *fiber.Ctx) error {
		// 다양한 레벨의 로그 생성
		levels := []string{"info", "warn", "error", "debug"}
		messages := []string{
			"User logged in successfully",
			"Database connection established",
			"Cache miss for key: user:123",
			"Payment processing completed",
			"API rate limit exceeded",
			"Database query timeout",
			"Memory usage high: 85%",
			"New user registration",
		}

		for i := 0; i < 10; i++ {
			level := levels[i%len(levels)]
			message := messages[i%len(messages)]

			sendLog(level, message, map[string]interface{}{
				"iteration":  i + 1,
				"user_id":    fmt.Sprintf("user_%d", 100+i),
				"request_id": fmt.Sprintf("req_%d", time.Now().UnixNano()),
			})

			time.Sleep(100 * time.Millisecond)
		}

		return c.JSON(fiber.Map{
			"message":   "Generated 10 sample logs",
			"timestamp": time.Now().Format(time.RFC3339),
		})
	})

	// 서버 시작
	port := getEnv("PORT", "8080")
	log.Printf("서버가 포트 %s에서 시작됩니다", port)
	log.Fatal(app.Listen(":" + port))
}

func sendLog(level, message string, fields map[string]interface{}) {
	logEntry := LogEntry{
		Timestamp: time.Now().Format(time.RFC3339),
		Level:     level,
		Message:   message,
		Service:   "go-server",
		Fields:    fields,
	}

	// JSON으로 직렬화
	jsonData, err := json.Marshal(logEntry)
	if err != nil {
		logrus.WithError(err).Error("로그 직렬화 실패")
		return
	}

	// Logstash로 전송
	if logstashConn != nil {
		_, err := logstashConn.Write(append(jsonData, '\n'))
		if err != nil {
			logrus.WithError(err).Error("Logstash 전송 실패")
		}
	}

	// 파일 로그 기록
	if fileLogger != nil {
		logLevel, _ := logrus.ParseLevel(level)
		fileLogger.WithFields(logrus.Fields(fields)).Log(logLevel, message)
	}

	// 로컬 로그도 출력
	logrus.WithFields(logrus.Fields(fields)).Log(logrus.InfoLevel, message)
}

func setupFileLogger(logDir string) *logrus.Logger {
	logger := logrus.New()

	// 로그 파일 경로 설정
	logFile := filepath.Join(logDir, "app.log")
	file, err := os.OpenFile(logFile, os.O_CREATE|os.O_WRONLY|os.O_APPEND, 0666)
	if err != nil {
		log.Printf("로그 파일 생성 실패: %v", err)
		return nil
	}

	// 멀티 라이터 설정 (콘솔 + 파일)
	multiWriter := io.MultiWriter(os.Stdout, file)
	logger.SetOutput(multiWriter)

	// JSON 포맷으로 설정
	logger.SetFormatter(&logrus.JSONFormatter{
		TimestampFormat: time.RFC3339,
	})

	// 로그 레벨 설정
	logger.SetLevel(logrus.InfoLevel)

	return logger
}

func getEnv(key, defaultValue string) string {
	if value := os.Getenv(key); value != "" {
		return value
	}
	return defaultValue
}
