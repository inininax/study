#!/bin/bash
# LangChain 기본기 학습 프로젝트 설정 스크립트

echo "🚀 LangChain 기본기 학습 프로젝트 설정을 시작합니다..."

# uv 설치 확인
if ! command -v uv &> /dev/null; then
    echo "📦 uv가 설치되어 있지 않습니다. 설치를 시작합니다..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    source $HOME/.cargo/env
    echo "✅ uv 설치 완료"
else
    echo "✅ uv가 이미 설치되어 있습니다"
fi

# Python 3.12 확인
echo "🐍 Python 버전 확인 중..."
python3 --version

# 가상환경 생성
echo "📁 가상환경 생성 중..."
uv venv --python 3.12 .venv

# 가상환경 활성화
echo "🔧 가상환경 활성화 중..."
source .venv/bin/activate

# 의존성 설치
echo "📚 의존성 설치 중..."
uv pip install -r requirements.txt

# 주피터 노트북 커널 등록
echo "📓 주피터 노트북 커널 등록 중..."
uv pip install ipykernel
python -m ipykernel install --user --name=langchain-basics --display-name="LangChain Basics"

echo "🎉 설정이 완료되었습니다!"
echo ""
echo "다음 명령어로 주피터 노트북을 실행하세요:"
echo "  source .venv/bin/activate"
echo "  jupyter notebook"
echo ""
echo "또는 다음 명령어로 바로 실행할 수 있습니다:"
echo "  ./run.sh"
