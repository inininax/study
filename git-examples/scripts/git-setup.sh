#!/bin/bash

# Git 초기 설정 및 리포지토리 설정 스크립트
# 사용법: ./git-setup.sh [repository-name] [remote-url]

set -e

REPO_NAME=${1:-"new-project"}
REMOTE_URL=${2:-""}

echo "🚀 Git 리포지토리 초기 설정을 시작합니다..."

# Git 초기화 (이미 초기화된 경우 무시)
if [ ! -d ".git" ]; then
    echo "📦 Git 리포지토리 초기화 중..."
    git init
    echo "✅ Git 리포지토리 초기화 완료"
else
    echo "📦 기존 Git 리포지토리 확인됨"
fi

# 기본 브랜치를 main으로 설정
echo "🌿 기본 브랜치를 main으로 설정..."
git config --global init.defaultBranch main
git branch -M main

# 기본 .gitignore 파일 생성 (없는 경우)
if [ ! -f ".gitignore" ]; then
    echo "📄 .gitignore 파일 생성 중..."
    cat > .gitignore << 'EOF'
# OS generated files
.DS_Store
.DS_Store?
._*
.Spotlight-V100
.Trashes
ehthumbs.db
Thumbs.db

# IDE
.vscode/
.idea/
*.swp
*.swo

# Logs
*.log
logs/

# Runtime data
pids
*.pid
*.seed
*.pid.lock

# Coverage directory used by tools like istanbul
coverage/
*.lcov

# Dependency directories
node_modules/
vendor/

# Optional npm cache directory
.npm

# Environment variables
.env
.env.local
.env.development.local
.env.test.local
.env.production.local

# Build outputs
dist/
build/
target/
bin/
EOF
    echo "✅ .gitignore 파일 생성 완료"
fi

# Remote URL이 제공된 경우 origin 설정
if [ ! -z "$REMOTE_URL" ]; then
    echo "🔗 Remote origin 설정 중..."
    if git remote get-url origin > /dev/null 2>&1; then
        git remote set-url origin "$REMOTE_URL"
        echo "✅ Origin URL 업데이트: $REMOTE_URL"
    else
        git remote add origin "$REMOTE_URL"
        echo "✅ Origin 추가: $REMOTE_URL"
    fi
fi

# 현재 상태 출력
echo ""
echo "📊 현재 Git 상태:"
git status

echo ""
echo "🎉 Git 설정이 완료되었습니다!"
echo "💡 다음 단계: git add . && git commit -m \"Initial commit\""
if [ ! -z "$REMOTE_URL" ]; then
    echo "💡 그 다음: git push -u origin main"
fi