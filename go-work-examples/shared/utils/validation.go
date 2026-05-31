package utils

import (
	"regexp"
	"strings"
)

var emailRegex = regexp.MustCompile(`^[a-z0-9._%+\-]+@[a-z0-9.\-]+\.[a-z]{2,}$`)

func IsValidEmail(email string) bool {
	return emailRegex.MatchString(strings.ToLower(email))
}

func IsValidName(name string) bool {
	return len(strings.TrimSpace(name)) >= 2
}

func ValidateRequired(value string) bool {
	return len(strings.TrimSpace(value)) > 0
}