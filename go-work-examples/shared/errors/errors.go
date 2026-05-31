package errors

import (
	"fmt"
	"net/http"
)

// Common error types for all services
type ValidationError struct {
	Message string `json:"message"`
	Field   string `json:"field,omitempty"`
}

func (e *ValidationError) Error() string {
	if e.Field != "" {
		return fmt.Sprintf("validation error in field '%s': %s", e.Field, e.Message)
	}
	return e.Message
}

func (e *ValidationError) HTTPStatus() int {
	return http.StatusBadRequest
}

type NotFoundError struct {
	Message string `json:"message"`
	ID      string `json:"id,omitempty"`
}

func (e *NotFoundError) Error() string {
	if e.ID != "" {
		return fmt.Sprintf("%s (ID: %s)", e.Message, e.ID)
	}
	return e.Message
}

func (e *NotFoundError) HTTPStatus() int {
	return http.StatusNotFound
}

type ConflictError struct {
	Message string `json:"message"`
	Field   string `json:"field,omitempty"`
}

func (e *ConflictError) Error() string {
	if e.Field != "" {
		return fmt.Sprintf("conflict in field '%s': %s", e.Field, e.Message)
	}
	return e.Message
}

func (e *ConflictError) HTTPStatus() int {
	return http.StatusConflict
}

type InternalError struct {
	Message string `json:"message"`
}

func (e *InternalError) Error() string {
	return e.Message
}

func (e *InternalError) HTTPStatus() int {
	return http.StatusInternalServerError
}

// HTTPError interface for consistent error handling
type HTTPError interface {
	error
	HTTPStatus() int
}

// NewValidationError creates a new validation error
func NewValidationError(message string) *ValidationError {
	return &ValidationError{Message: message}
}

// NewValidationErrorWithField creates a new validation error with field context
func NewValidationErrorWithField(field, message string) *ValidationError {
	return &ValidationError{Message: message, Field: field}
}

// NewNotFoundError creates a new not found error
func NewNotFoundError(message string) *NotFoundError {
	return &NotFoundError{Message: message}
}

// NewNotFoundErrorWithID creates a new not found error with ID context
func NewNotFoundErrorWithID(id, message string) *NotFoundError {
	return &NotFoundError{Message: message, ID: id}
}

// NewConflictError creates a new conflict error
func NewConflictError(message string) *ConflictError {
	return &ConflictError{Message: message}
}

// NewConflictErrorWithField creates a new conflict error with field context
func NewConflictErrorWithField(field, message string) *ConflictError {
	return &ConflictError{Message: message, Field: field}
}

// NewInternalError creates a new internal error
func NewInternalError(message string) *InternalError {
	return &InternalError{Message: message}
}
