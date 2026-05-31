#!/bin/bash

# Go Workspace 모든 모듈 정리 스크립트
echo "🧹 Go Workspace 모든 모듈 정리 시작..."

# 워크스페이스 루트로 이동
cd "$(dirname "$0")/.."

echo "📦 워크스페이스 동기화..."
go work sync

echo "🧹 각 모듈 정리..."

# Services
echo "  - services/user-service"
cd services/user-service && go mod tidy && go clean -cache && cd ../..

echo "  - services/order-service"  
cd services/order-service && go mod tidy && go clean -cache && cd ../..

echo "  - services/notification-service"
cd services/notification-service && go mod tidy && go clean -cache && cd ../..

# Tools
echo "  - tools/cli"
cd tools/cli && go mod tidy && go clean -cache && cd ../..

echo "  - tools/migration"
cd tools/migration && go mod tidy && go clean -cache && cd ../..

# Examples
echo "  - examples/library-consumer"
cd examples/library-consumer && go mod tidy && go clean -cache && cd ../..

echo "  - examples/workspace-demo"
cd examples/workspace-demo && go mod tidy && go clean -cache && cd ../..

echo "✅ 모든 모듈 정리 완료!"
