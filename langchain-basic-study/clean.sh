#!/bin/bash
# LangChain 기본기 학습 프로젝트 정리 스크립트

echo "🧹 프로젝트 정리를 시작합니다..."

# 가상환경 제거
if [ -d ".venv" ]; then
    echo "🗑️ 가상환경 제거 중..."
    rm -rf .venv
    echo "✅ 가상환경 제거 완료"
fi

# __pycache__ 제거
if [ -d "__pycache__" ]; then
    echo "🗑️ Python 캐시 파일 제거 중..."
    find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
    echo "✅ Python 캐시 파일 제거 완료"
fi

# .ipynb_checkpoints 제거
if [ -d ".ipynb_checkpoints" ]; then
    echo "🗑️ 주피터 노트북 체크포인트 제거 중..."
    find . -type d -name ".ipynb_checkpoints" -exec rm -rf {} + 2>/dev/null || true
    echo "✅ 주피터 노트북 체크포인트 제거 완료"
fi

# 로그 파일 제거
echo "🗑️ 로그 파일 제거 중..."
find . -name "*.log" -delete 2>/dev/null || true
find . -name "*.tmp" -delete 2>/dev/null || true

echo "🎉 정리가 완료되었습니다!"
echo ""
echo "다시 시작하려면 다음 명령어를 실행하세요:"
echo "  ./setup.sh"
