package main

import (
	"errors"
	"math"
)

var (
	ErrNegativeInput  = errors.New("음수는 입력할 수 없습니다")
	ErrUint64Overflow = errors.New("결과가 uint64 범위를 초과합니다")
)

// Fibonacci 함수는 n번째 피보나치 수를 계산합니다.
// n이 음수이거나 결과가 uint64를 초과하면 에러를 반환합니다.
func Fibonacci(n int) (uint64, error) {
	if n < 0 {
		return 0, ErrNegativeInput
	}
	if n <= 1 {
		return uint64(n), nil
	}

	var prev, current uint64 = 0, 1
	for i := 2; i <= n; i++ {
		// 오버플로우 체크
		next, overflow := addUint64(prev, current)
		if overflow {
			return 0, ErrUint64Overflow
		}
		prev, current = current, next
	}
	return current, nil
}

// addUint64는 두 uint64 값을 더하고 오버플로우 여부를 반환합니다.
func addUint64(a, b uint64) (uint64, bool) {
	if b > math.MaxUint64-a {
		return 0, true
	}
	return a + b, false
}
