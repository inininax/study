#!/bin/bash

# Go Workspace 전체 동기화 스크립트
echo "🔄 Go Workspace 전체 동기화 시작..."

# 워크스페이스 루트로 이동
cd "$(dirname "$0")/.."

echo "📦 워크스페이스 동기화..."
go work sync

echo "🧹 각 모듈 의존성 정리..."

# Services
echo "  - services/user-service"
cd services/user-service && go mod tidy && cd ../..

echo "  - services/order-service"  
cd services/order-service && go mod tidy && cd ../..

echo "  - services/notification-service"
cd services/notification-service && go mod tidy && cd ../..

# Tools
echo "  - tools/cli"
cd tools/cli && go mod tidy && cd ../..

echo "  - tools/migration"
cd tools/migration && go mod tidy && cd ../..

# Examples
echo "  - examples/library-consumer"
cd examples/library-consumer && go mod tidy && cd ../..

echo "  - examples/workspace-demo"
cd examples/workspace-demo && go mod tidy && cd ../..

echo "✅ 모든 모듈 동기화 완료!"
echo ""
echo "📋 사용 가능한 명령어:"
echo "  ./scripts/sync-all.sh     - 전체 동기화"
echo "  ./scripts/update-all.sh   - 모든 의존성 업데이트"
echo "  ./scripts/clean-all.sh    - 모든 모듈 정리"
