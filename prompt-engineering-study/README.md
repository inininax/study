# Prompt Engineering

## Examples
```text
Frame
    A person in a Grocery Store
Subject
    A woman pick an apple
Style
    In Van Gogh style
```

## LLM
- Zero-shot
  - 명령어 only
- One-shot learning
  - 명령어 + 예제 제시
- Few-shot learnin
  - 명령어 + 예제 제시
- Chain of Thought
  - 문제 해결 가이드 제공
- Zero Shot Chain of Thought
  - 문제 답변을 직접적으로 제시하지 않고 지속적으로 생각하게 하는 것

> 사용자 입력 > 검색 등 추가 작업 > LLM을 통한 답변

## Vector Search
- Text > Embedding model (BERT, GPT) > Text as vector
- 키워드의 유사 관련도가 1000차원 이상으로 구성되어 사람이 읽을 수 없을 정보
- 남자 - 킹 , 여자 - 퀸 , 킹+퀸 -> 왕족 , 남자 != 여자와 같이 관련성의 군집
- Embedding Space, 실수의 집합
- Sentence Embedding
- Semantic Search

## Prompt Design Framework
- 답변을 위해 필요한 적절한 컨텍스트 제공
- 원하는 결과를 추출을 위한 프롬프트 작성
- 원하는 포맷의 출력을 위한 프롬프트 작성

### 프롬프트 구성요소
- Role
  - 답변자로써의 페르소나 설정
- Audience
  - 답변을 듣는 대상자 설정
- Knowledge
  - 답변의 참고할 만한 자료 제공 (중요)
- Task
  - 특정 작업이나 목표
- Policy (Rule) 
  - 특정 정책이나 규칙
  - Style: 특정 톤, 유머, 감정 등의 스타일
  - Constraint: 응답이 따라야하는 특정 제한 사항이나 조건
- Format
  - 응답이 따라야 하는 특정 형식이나 구조
  - Formatting
    - 출력 포맷 지정
    - 릭스트
      - 일반 리스트
      - 순서 있는 리스트
    - Key-Value Pair
    - 테이블
    - 마크다운
    - YAML
    - JSON
- Examples
  - 원하는 답변의 예시를 제공

### Prompt Spec.
- Role: 영어 선생님
- Audience: 초등학교 학생들
- Knowledge: 나폴레옹 본다파르트에 대한 지식
- Task: 나폴레옹 본다파르트에 대한 설명하는 것
- Policy: 단순하고 이해하기 쉬운 언어 사용
- Style: 친근하고 교육적인 톤
- Constraint: 3분 안에 읽을 수 있는 길이로, 영어로 작성
- Format: 대화 형식으로 작성
- Example:
  - User: 나폴레옹이 누구야?
  - Assistant: 나폴레옹 본다파르트는 18세기 후반과 19세기 초에 프랑스를 지배한...

### Prompt Ver. 1
```text
당신은 친근한 영어 선생님입니다.

학생들에게 나폴레옹 본다파르트에 대해 친근하고 교육적인 톤으로, 단순하고 이해하기 쉬운 영어로 설명해 주세요.
위키피디아의 설명을 참고해서 대답해 주세요.

설명은 3분 안에 읽을 수 있는 길이로 제한되어야 하며, 학생들이 이해하기 쉬워야 합니다.
아래 예시를 참고하여 대화 형식으로 작성해 주세요.

User: 나폴레옹이 누구야?
Assistant: 나폴레옹 본다파르트는 18세기 후반과 19세기 초에 프랑스를 지배한...
```

### Prompt Ver. 2
```text
당신은 친근한 영어 선생님입니다.
다음의 내용을 참고하여 학생들에게 나폴레옹 본다파르트에 대해 설명해 주세요.

--

[아래는 나폴레옹에 대한 정보]
...

---

다음의 규칙에 따라 답변을 작성해 주세요.
- 친근하고 교육적인 톤으로 작성
- 단순하고 이해하기 쉬운 영어로 설명
- 3분 안에 읽을 수 있는 길이로 작성
- 세 문단으로 작성

결괄 포맷:
User: 나폴레옹이 누구야?
Assistant: 나폴레옹 본다파르트는 18세기 후반과 19세기 초에 프랑스를 지배한...
```

## 프롬프트 테크닉 TOP 7
- Few-shot examples
- Chain-of-Thought (COT): 답변을 만드는 과정을 질의
- Self-Consistency: 여러개의 COT를 제공
- Selection-Inference: 선택(selection) <> 추론을 번갈아 가면 답변을 추론
- Least-to-Most: 하나의 문제를 더 작은 문제로 분할
- ReAct: 실행 계획을 유도하고 추적하여 작업벼로 실행할 액션을 선택하고 실행하는 방법
- Self Evaluation: LLM이 생성한 결과를 LLM이 평가하게 하여, 오류를 잡거나 결과를 향상 시키는 방법, 스스로 평가

## 프롬프트 테크닉 확장 테크닉
- Expert Prompting
- According to Wikipedia
- Generated Knowledge Prompting
- Retrieval Augmented Generation (RAG)
- Tree-of-Thought
- Plan-and-Solve Prompting
- Automatic Prompt Engineer

## 실습 도구
- OpenAI Playground
- Google Colab

## LLM 생성 조건 이해하기
- Token
- Context Window: 문맥을 판단하거나 다음 단어를 예측하기 위해 참고할 토큰 범위
- 주요 생성 옵션
  - (가장 많이 사용) Temperature: 출력할 토큰의 확률을 선택하는 방식, 높을 수록 원하지 않는 결과를 출력할 가능성이 큼, 0.1 정도로 사용, 값이 높아질 수록 오탑 확률 증가
  - Top P, Top K: 모델이 다음 토큰 후보를 선택하는 방식
  - (가장 많이 사용) Maximum length: 생성할 최대 토큰 수
  - Frequency Penalty: 같은 토큰을 반복하면 패널티를 주는 파라미터
  - Presence Penalty: 한번 이상 샘플링 된 토큰에 패널티를 주는 파라미터
  - Stop sequence: 특정 문구를 설정하고 해당 문구가 나오면 생성을 중지
  - Injection Start: 생성 전 특정한 문구를 삽입하고 생성을 시작함, 다음 생성 결과를 원하는대로 유도 가능

## 자연어 처리 태스크
- Text Generation
  - Language Translation: 한 언에서 다른 언어로 번역
  - Style Translation: 텍스트 스타일을 변경 ex) 비격식을 격식으로 변경
  - Editing and Rewriting: 의도를 더 잘 전달하도록 문장 또는 문서를 수정 혹은 재작성
  - Summarization: 긴 텍스트를 핵심 내용을 포함하는 짧은 텍스트로 축소, 내용 요약
- Text Analysis
  - Named Entity Recognition(인지도): 텍스트에서 특정 정보를 식별하는 작업
  - Sentiment Recognition: 긍정적, 부정적, 중립적 등 텍스트의 다양한 감정 상태를 판단하는 작업
  - Document Classification(분류): 텍스트 문서를 사전 정의된 카테고리 또는 클래스로 분류
  - Topic Modeling: 문서 집합에서 주제를 발견하고 각 문서에 주제를 할당하는 작업
  - Similarity Evaluation(유사성 평가): 두 개의 텍스트 사이의 유사성을 측정하는 작업
  - Question Answering: 주어진 텍스트에서 질문에 대한 정보를 찾아 답변하는 작업

## 프롬프트 테크닉
- 예시 사용
- 액팅
- 포맷팅

## 프롬프트 체이닝
- 프롬프트와 그에 따른 응답을 수서대로 연결
- 하나의 지속적인 대화나 여러 하위 태스크로 복잡한 태스크를 수행하는 기법
- Self-Consistency
- Selection-Inference
- Least-to-Most
- ReAct
- 모두 프롬프트 체이닝을 사용

## 좋은 프롬프트 만들기
- 과정
  1. 지시문을 명확하게 만든다.
  2, 적절한 예시를 제공한다.
  3. 모델에게 생각할 시간을 준다.
  4. 작업을 하위 작업으로 분해한다.
  5. 적절한 컨텍스트를 제공한다.
  6. 프롬프트 엔지니어링 기법이 작동하지 않을 수 있다.
  7. 프롬프트를 구조화하여 작성한다. (코드와 유사한 형식으로 작성)
- 반복적 개선이 필요하며 시행착오를 많이 겪는다.
- 반복하고 개선하라.

## 적합한 모델 선택하기
- 모델 선택 기준
  1. 비용
  2. 속도
  3. 정확도 (성능)
  4. 경향성
  5. 안전성
  6. API 안전성
  7. 보안
- 토크나이저를 통해 입력 토큰, 출력 토큰 수를 계산
- 벤치마크마다 성능이 다를 수 있다.
- 정확도와 경향성이 가장 중요
- 모델이 업그레이드 될 경우 API 안전성에 문제가 생길 수 있음.



