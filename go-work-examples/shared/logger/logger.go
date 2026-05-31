package logger

import (
	"encoding/json"
	"fmt"
	"log"
	"os"
	"time"
)

// LogLevel represents the logging level
type LogLevel int

const (
	DEBUG LogLevel = iota
	INFO
	WARN
	ERROR
)

// String returns the string representation of LogLevel
func (l LogLevel) String() string {
	switch l {
	case DEBUG:
		return "DEBUG"
	case INFO:
		return "INFO"
	case WARN:
		return "WARN"
	case ERROR:
		return "ERROR"
	default:
		return "UNKNOWN"
	}
}

// LogEntry represents a structured log entry
type LogEntry struct {
	Timestamp time.Time              `json:"timestamp"`
	Level     string                 `json:"level"`
	Message   string                 `json:"message"`
	Service   string                 `json:"service,omitempty"`
	Fields    map[string]interface{} `json:"fields,omitempty"`
}

// Logger provides structured logging functionality
type Logger struct {
	service string
	level   LogLevel
	format  string
}

// NewLogger creates a new logger instance
func NewLogger(service string, level LogLevel, format string) *Logger {
	return &Logger{
		service: service,
		level:   level,
		format:  format,
	}
}

// Debug logs a debug message
func (l *Logger) Debug(message string, fields ...map[string]interface{}) {
	l.log(DEBUG, message, fields...)
}

// Info logs an info message
func (l *Logger) Info(message string, fields ...map[string]interface{}) {
	l.log(INFO, message, fields...)
}

// Warn logs a warning message
func (l *Logger) Warn(message string, fields ...map[string]interface{}) {
	l.log(WARN, message, fields...)
}

// Error logs an error message
func (l *Logger) Error(message string, fields ...map[string]interface{}) {
	l.log(ERROR, message, fields...)
}

// log is the internal logging method
func (l *Logger) log(level LogLevel, message string, fields ...map[string]interface{}) {
	if level < l.level {
		return
	}

	entry := LogEntry{
		Timestamp: time.Now(),
		Level:     level.String(),
		Message:   message,
		Service:   l.service,
	}

	if len(fields) > 0 {
		entry.Fields = fields[0]
	}

	if l.format == "json" {
		l.logJSON(entry)
	} else {
		l.logText(entry)
	}
}

// logJSON outputs log in JSON format
func (l *Logger) logJSON(entry LogEntry) {
	data, err := json.Marshal(entry)
	if err != nil {
		log.Printf("Failed to marshal log entry: %v", err)
		return
	}
	fmt.Fprintln(os.Stdout, string(data))
}

// logText outputs log in text format
func (l *Logger) logText(entry LogEntry) {
	timestamp := entry.Timestamp.Format("2006-01-02 15:04:05")
	fieldsStr := ""
	if entry.Fields != nil && len(entry.Fields) > 0 {
		fieldsStr = fmt.Sprintf(" %+v", entry.Fields)
	}
	fmt.Fprintf(os.Stdout, "[%s] %s %s: %s%s\n",
		timestamp, entry.Level, entry.Service, entry.Message, fieldsStr)
}

// WithFields creates a new logger with additional fields
func (l *Logger) WithFields(fields map[string]interface{}) *Logger {
	return &Logger{
		service: l.service,
		level:   l.level,
		format:  l.format,
	}
}

// SetLevel changes the logging level
func (l *Logger) SetLevel(level LogLevel) {
	l.level = level
}

// DefaultLogger returns a default logger instance
func DefaultLogger(service string) *Logger {
	level := INFO
	if os.Getenv("LOG_LEVEL") == "debug" {
		level = DEBUG
	}
	format := "text"
	if os.Getenv("LOG_FORMAT") == "json" {
		format = "json"
	}
	return NewLogger(service, level, format)
}
