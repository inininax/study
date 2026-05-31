FROM golang:1.22 AS builder

WORKDIR /app

COPY go.mod go.sum ./
RUN go mod download

COPY . .

RUN CGO_ENABLED=0 GOOS=linux GOARCH=amd64 go build -o es-examples ./cmd/es-examples

FROM gcr.io/distroless/base-debian12

WORKDIR /app

COPY --from=builder /app/es-examples .

ENV ELASTICSEARCH_URL=http://elasticsearch:9200

ENTRYPOINT ["./es-examples"]

