# 01. Python 소개 및 환경 설정

## 🎯 학습 목표
- Python이 무엇이며 왜 인기 있는지 이해한다
- 자신의 컴퓨터에 Python 개발 환경을 구축한다
- 첫 Python 프로그램을 작성하고 실행한다

## 1. Python이란?

**Python**은 1991년 네덜란드 개발자 **귀도 반 로섬(Guido van Rossum)** 이 발표한 고급 프로그래밍 언어입니다.

### Python의 특징
- **읽기 쉬운 문법**: 영어와 비슷한 자연스러운 문법
- **인터프리터 언어**: 컴파일 없이 즉시 실행
- **동적 타이핑**: 변수 타입을 미리 선언할 필요 없음
- **풍부한 라이브러리**: 다양한 분야의 검증된 라이브러리
- **크로스 플랫폼**: Windows, macOS, Linux 모두 지원

### Python이 사용되는 분야
- 🌐 **웹 개발**: Django, Flask, FastAPI
- 📊 **데이터 분석**: pandas, NumPy
- 🤖 **머신러닝/AI**: TensorFlow, PyTorch, scikit-learn
- 🔧 **자동화**: 시스템 관리, 웹 크롤링
- 🎮 **게임 개발**: Pygame
- 🔬 **과학 계산**: SciPy, Matplotlib

## 2. Python 설치

### Windows
1. [python.org/downloads](https://www.python.org/downloads/) 접속
2. 최신 Python 3.x 다운로드
3. 설치 시 **"Add Python to PATH"** 체크 필수
4. 설치 확인:
```bash
python --version
```

### macOS
```bash
# Homebrew 사용 (권장)
brew install python@3.12

# 또는 공식 사이트에서 다운로드
```

### Linux (Ubuntu/Debian)
```bash
sudo apt update
sudo apt install python3 python3-pip
```

### 설치 확인
```bash
python3 --version
# 출력 예: Python 3.12.0

pip3 --version
# 출력 예: pip 23.x.x
```

## 3. 개발 환경 선택

### 추천 에디터/IDE

#### 🥇 VS Code (초보자 추천)
- 무료, 가벼움, 확장성 우수
- Python 확장 설치 필수
- [code.visualstudio.com](https://code.visualstudio.com/)

#### 🥈 PyCharm
- 강력한 기능, 디버깅 우수
- Community 버전은 무료
- [jetbrains.com/pycharm](https://www.jetbrains.com/pycharm/)

#### 🥉 Jupyter Notebook
- 데이터 분석/학습에 최적
- 셀 단위 실행 가능
```bash
pip install jupyter
jupyter notebook
```

## 4. 가상 환경 설정

프로젝트별로 패키지를 독립적으로 관리하기 위해 **가상 환경**을 사용합니다.

```bash
# 가상 환경 생성
python3 -m venv myenv

# 활성화 (macOS/Linux)
source myenv/bin/activate

# 활성화 (Windows)
myenv\Scripts\activate

# 비활성화
deactivate
```

### 패키지 관리
```bash
# 패키지 설치
pip install requests

# 설치된 패키지 목록
pip list

# 요구사항 파일 생성
pip freeze > requirements.txt

# 요구사항 파일로 일괄 설치
pip install -r requirements.txt
```

## 5. 첫 Python 프로그램

### Hello, World!
파일을 만들고 `hello.py` 라고 저장하세요.

```python
# hello.py
print("Hello, World!")
print("안녕하세요, Python!")
```

### 실행 방법
```bash
python3 hello.py
```

### 출력
```
Hello, World!
안녕하세요, Python!
```

## 6. 대화형 인터프리터 (REPL)

터미널에서 `python3` 만 입력하면 대화형 모드로 진입합니다.

```pycon
>>> 1 + 1
2
>>> print("Hello")
Hello
>>> name = "Python"
>>> print(f"I love {name}!")
I love Python!
>>> exit()  # 또는 Ctrl+D
```

## 7. Python의 Zen (선)

Python의 철학을 확인해보세요.

```pycon
>>> import this
```

주요 원칙:
- **Beautiful is better than ugly** (아름다운 것이 추한 것보다 낫다)
- **Explicit is better than implicit** (명시적인 것이 암시적인 것보다 낫다)
- **Simple is better than complex** (단순함이 복잡함보다 낫다)
- **Readability counts** (가독성은 중요하다)

## 8. 첫 인터랙티브 프로그램

```python
# greeting.py
name = input("이름을 입력하세요: ")
age = input("나이를 입력하세요: ")
print(f"안녕하세요, {name}님! {age}살이시군요.")
```

## 📝 연습 문제

### 문제 1: 환경 확인
터미널에서 다음 명령을 실행하고 결과를 확인하세요.
```bash
python3 --version
pip3 --version
```

### 문제 2: 자기소개 프로그램
사용자에게 이름, 나이, 취미를 입력받아 다음과 같이 출력하는 프로그램을 작성하세요.
```
=== 자기소개 ===
이름: 홍길동
나이: 25
취미: 코딩
```

### 문제 3: 가상 환경 만들기
`python-study` 라는 가상 환경을 만들고 활성화한 후, `requests` 패키지를 설치해보세요.

## ✅ 체크리스트
- [ ] Python 3.x가 설치되어 있다
- [ ] 에디터(VS Code 등)가 설치되어 있다
- [ ] `hello.py` 를 작성하고 실행할 수 있다
- [ ] 가상 환경을 만들 수 있다
- [ ] `pip` 으로 패키지를 설치할 수 있다

## 🔗 다음 챕터
👉 [02. 변수와 데이터 타입](./02-variables-and-types.md)
