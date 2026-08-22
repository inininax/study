# LangChain 기본기 학습 프로젝트

## 📚 프로젝트 개요
- **강의명**: 한시간으로 끝내는 LangChain 기본기
- **목표**: LangChain의 핵심 개념을 실습을 통해 학습
- **Python 버전**: 3.12+
- **패키지 관리**: uv (권장) 또는 pip

## 🚀 1. 프로젝트 설정

### 필수 요구사항
- Python 3.12 이상
- uv (권장) 또는 pip
- Ollama (로컬 모델 사용 시)

### 빠른 시작
```bash
# 1. 프로젝트 설정 (최초 1회)
./setup.sh

# 2. 주피터 노트북 실행
./run.sh
```

### 수동 설정
```bash
# uv 사용 (권장)
uv venv --python 3.12 .venv
source .venv/bin/activate
uv pip install -r requirements.txt

# 또는 pip 사용
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Ollama 설정 (로컬 모델 사용 시)
```bash
# Ollama 설치 및 모델 다운로드
brew install ollama
ollama pull gemma3:1b
ollama serve
```

## 📖 2. 학습 노트북 가이드

### 01_chat.ipynb - LLM 기본 사용법
**핵심 내용**: 다양한 LLM 모델을 사용한 기본적인 채팅 구현

**학습 포인트**:
- **Ollama (로컬)**: `ChatOllama`를 사용한 로컬 모델 호출
- **OpenAI (클라우드)**: `ChatOpenAI`를 사용한 클라우드 모델 호출
- **Azure OpenAI**: `AzureChatOpenAI`를 사용한 엔터프라이즈 모델 호출 (`.env`에 `AZURE_OPENAI_*` 변수 필요, `.env.example` 참고)

**주요 코드**:
```python
# 로컬 모델
from langchain_ollama import ChatOllama
llm = ChatOllama(model="gemma3:1b")
response = llm.invoke("너는 누구냐?")

# 클라우드 모델
from langchain_openai import ChatOpenAI
llm = ChatOpenAI(model="gpt-4o-mini")
response = llm.invoke("너는 누구냐?")
```

### 02_prompt.ipynb - 프롬프트 템플릿 활용
**핵심 내용**: LangChain의 프롬프트 템플릿 시스템 학습

**학습 포인트**:
- **PromptTemplate**: 기본 템플릿 생성 및 사용
- **ChatPromptTemplate**: 대화형 프롬프트 템플릿
- **Message Types**: HumanMessage, AIMessage, SystemMessage 활용

**주요 코드**:
```python
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate

# 기본 템플릿
prompt_template = PromptTemplate(
    input_variables=["country"], 
    template="What is the capital of {country}?"
)

# 채팅 템플릿
chat_template = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant."),
    ("human", "What is the capital of {country}?")
])
```

### 03_output_parser.ipynb - 출력 파싱 및 구조화
**핵심 내용**: LLM 응답을 구조화된 데이터로 변환하는 방법

**학습 포인트**:
- **StrOutputParser**: 문자열 출력 파싱
- **Pydantic 모델**: 구조화된 출력 정의
- **with_structured_output**: 자동 구조화 출력

**주요 코드**:
```python
from langchain_core.output_parsers import StrOutputParser
from pydantic import BaseModel, Field

# 기본 파서
output_parser = StrOutputParser()
result = output_parser.invoke(llm_response)

# 구조화된 출력
class CountryDetail(BaseModel):
    capital: str = Field(description="The capital of the country")
    population: int = Field(description="The population of the country")

structured_llm = llm.with_structured_output(CountryDetail)
```

### 04_runnable.ipynb - 체인(Chain) 구성
**핵심 내용**: LangChain의 핵심인 Runnable과 체인 구성

**학습 포인트**:
- **Runnable 파이프라인**: `|` 연산자를 사용한 체인 구성
- **RunnablePassthrough**: 데이터 전달 및 변환
- **복합 체인**: 여러 체인을 연결한 복잡한 워크플로우

**주요 코드**:
```python
from langchain_core.runnables import RunnablePassthrough

# 기본 체인
chain = prompt_template | llm | output_parser

# 복합 체인
final_chain = (
    {"information": RunnablePassthrough()}
    | {"country": country_chain}
    | capital_chain
)
```

## 🎯 3. 최종 프로젝트: 05_review.ipynb

### 프로젝트 개요
**"국가별 인기 음식과 레시피 추천 시스템"**을 LangChain으로 구현한 종합 프로젝트입니다.

### 🍽️ 구현된 기능

#### 1. 음식 추천 시스템
```python
food_prompt = PromptTemplate(
    template="""What is one of the most popular food in {country}?
    Please return the name of the food only""",
    input_variables=["country"],
)

food_chain = food_prompt | llm | StrOutputParser()
```

#### 2. 레시피 생성 시스템
```python
recipe_prompt = ChatPromptTemplate.from_messages([
    ("system", """Provide the recipe of the food that the user wants.
Please return the recipe only as a numbered list"""),
    ("human", "Can you give me the recipe for making {food}?"),
])

recipe_chain = recipe_prompt | llm | StrOutputParser()
```

#### 3. 통합 체인 시스템
```python
# 두 체인을 연결하여 완전한 워크플로우 구성
final_chain = {"food": food_chain} | recipe_chain

# 사용 예시
result = final_chain.invoke({"country": "South Korea"})
# 출력: 한국의 인기 음식(비빔밥)과 그 레시피를 자동으로 생성
```

### 🚀 핵심 학습 성과

#### **LangChain 핵심 개념 완전 이해**
1. **LLM 통합**: Ollama, OpenAI 등 다양한 모델 활용
2. **프롬프트 엔지니어링**: 효과적인 프롬프트 템플릿 설계
3. **출력 구조화**: Pydantic을 활용한 데이터 검증
4. **체인 구성**: Runnable을 통한 모듈화된 워크플로우

#### **실무 적용 가능한 패턴**
- **모듈화**: 각 기능을 독립적인 체인으로 분리
- **재사용성**: 템플릿과 체인의 조합으로 다양한 시나리오 대응
- **확장성**: 새로운 체인 추가로 기능 확장 용이
- **에러 처리**: 각 단계별 검증 및 오류 처리

### 🎓 학습 체크리스트

#### **기본 개념**
- [ ] LLM 모델 초기화 및 호출
- [ ] 프롬프트 템플릿 생성 및 활용
- [ ] 출력 파서를 통한 데이터 변환
- [ ] 체인 구성 및 실행

#### **고급 활용**
- [ ] 구조화된 출력 생성
- [ ] 복합 체인 구성
- [ ] 데이터 전달 및 변환
- [ ] 실무 프로젝트 구현

#### **실무 적용**
- [ ] 모듈화된 코드 설계
- [ ] 재사용 가능한 컴포넌트 개발
- [ ] 확장 가능한 아키텍처 구축
- [ ] 에러 처리 및 검증 로직

## 🛠️ 개발 환경

### 프로젝트 구조
```
langchain-basics-study/
├── 01_chat.ipynb          # LLM 기본 사용법
├── 02_prompt.ipynb        # 프롬프트 템플릿
├── 03_output_parser.ipynb # 출력 파싱
├── 04_runnable.ipynb      # 체인 구성
├── 05_review.ipynb        # 최종 프로젝트
├── requirements.txt       # 의존성 관리
├── setup.sh               # 프로젝트 설정
├── run.sh                 # 실행 스크립트
└── clean.sh               # 정리 스크립트
```

### 편의 스크립트
```bash
# 프로젝트 설정
./setup.sh

# 주피터 노트북 실행
./run.sh

# 프로젝트 정리
./clean.sh
```

## 🔧 환경 설정 체크리스트

### 기본 환경
- [ ] Python 3.12 이상 설치
- [ ] uv 설치 (`curl -LsSf https://astral.sh/uv/install.sh | sh`)
- [ ] 가상환경 생성 및 활성화
- [ ] 의존성 설치 (`uv pip install -r requirements.txt`)
- [ ] 주피터 노트북 실행

### 서비스 설정
- [ ] 환경변수 설정 (.env 파일)
- [ ] Ollama 서비스 실행 (로컬 모델 사용 시)
- [ ] API 키 설정 (클라우드 모델 사용 시)

## 🎉 결론

이 프로젝트를 통해 LangChain의 핵심 개념을 단계별로 학습하고, 최종적으로 **실제 사용 가능한 AI 애플리케이션**을 구현할 수 있습니다. 

**05_review.ipynb**는 단순한 학습을 넘어서 **실무에서 바로 활용할 수 있는 패턴**을 보여주며, LangChain의 진정한 가치인 **모듈화, 재사용성, 확장성**을 체험할 수 있는 완성도 높은 프로젝트입니다.

---

**🚀 지금 바로 시작하세요!**
```bash
./setup.sh && ./run.sh
```