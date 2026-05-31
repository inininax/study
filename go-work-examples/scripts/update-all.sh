#!/bin/bash

# Go Workspace 모든 의존성 업데이트 스크립트
echo "🔄 Go Workspace 모든 의존성 업데이트 시작..."

# 워크스페이스 루트로 이동
cd "$(dirname "$0")/.."

echo "📦 워크스페이스 동기화..."
go work sync

echo "⬆️ 각 모듈 의존성 업데이트..."

# Services
echo "  - services/user-service"
cd services/user-service && go get -u ./... && go mod tidy && cd ../..

echo "  - services/order-service"  
cd services/order-service && go get -u ./... && go mod tidy && cd ../..

echo "  - services/notification-service"
cd services/notification-service && go get -u ./... && go mod tidy && cd ../..

# Tools
echo "  - tools/cli"
cd tools/cli && go get -u ./... && go mod tidy && cd ../..

echo "  - tools/migration"
cd tools/migration && go get -u ./... && go mod tidy && cd ../..

# Examples
echo "  - examples/library-consumer"
cd examples/library-consumer && go get -u ./... && go mod tidy && cd ../..

echo "  - examples/workspace-demo"
cd examples/workspace-demo && go get -u ./... && go mod tidy && cd ../..

echo "✅ 모든 의존성 업데이트 완료!"
