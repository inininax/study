package main

import (
	"testing"
)

func TestFibonacci(t *testing.T) {
	tests := []struct {
		name    string
		input   int
		want    uint64
		wantErr error
	}{
		{"0번째 수", 0, 0, nil},
		{"1번째 수", 1, 1, nil},
		{"2번째 수", 2, 1, nil},
		{"3번째 수", 3, 2, nil},
		{"7번째 수", 7, 13, nil},
		{"10번째 수", 10, 55, nil},
		{"음수 입력", -1, 0, ErrNegativeInput},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			got, err := Fibonacci(tt.input)
			if err != tt.wantErr {
				t.Errorf("Fibonacci(%d) 에러 = %v, 원하는 에러 = %v", tt.input, err, tt.wantErr)
				return
			}
			if err == nil && got != tt.want {
				t.Errorf("Fibonacci(%d) = %v, 원하는 값 = %v", tt.input, got, tt.want)
			}
		})
	}

	// 오버플로우 테스트
	t.Run("큰 수 오버플로우 테스트", func(t *testing.T) {
		_, err := Fibonacci(94) // 94번째 피보나치 수는 uint64를 초과합니다
		if err != ErrUint64Overflow {
			t.Errorf("큰 수에서 오버플로우 에러가 발생해야 합니다")
		}
	})
}
