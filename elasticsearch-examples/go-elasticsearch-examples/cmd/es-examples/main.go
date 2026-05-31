package main

import (
	"context"
	"log"

	"elasticsearch-examples/internal/app"
)

func main() {
	if err := app.Run(context.Background()); err != nil {
		log.Printf("application terminated with error: %v", err)
	}
}


