package utils

import (
	"fmt"
)

func Hello() {
	fmt.Println("Hello")
}

func Say() {
	fmt.Println("Say")
	foo()
}

func foo() {
	fmt.Println("foo")
}
