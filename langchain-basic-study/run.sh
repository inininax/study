#!/bin/bash
# LangChain 기본기 학습 프로젝트 실행 스크립트

echo "🚀 LangChain 기본기 학습 프로젝트를 시작합니다..."

# 가상환경 활성화
if [ -d ".venv" ]; then
    echo "🔧 가상환경 활성화 중..."
    source .venv/bin/activate
else
    echo "❌ 가상환경이 없습니다. 먼저 ./setup.sh를 실행하세요."
    exit 1
fi

# 의존성 확인
echo "📚 의존성 확인 중..."
uv pip list | grep -E "(langchain|jupyter|ipykernel)" || {
    echo "📦 의존성을 설치합니다..."
    uv pip install -r requirements.txt
}

# 주피터 노트북 실행
echo "📓 주피터 노트북을 실행합니다..."
echo "브라우저에서 http://localhost:8888 로 접속하세요."
echo "종료하려면 Ctrl+C를 누르세요."
echo ""

jupyter notebook
