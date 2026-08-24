# 💪 연습 문제

학습한 내용을 실습으로 확인하는 연습 문제 모음입니다.

## 구조
```
exercises/
├── 01-beginner/        # 초급 연습 문제 + solutions.py
├── 02-intermediate/    # 중급 연습 문제 + solutions.py
├── 03-advanced/        # 고급 연습 문제 + solutions.py
└── 04-expert/          # 전문가 연습 문제 + solutions.py
```

## 학습 방법

### 1. 문제 풀기
각 챕터를 학습한 후 해당 폴더의 문제를 풀어보세요.

### 2. 직접 작성
```bash
cd 01-beginner
# 새 파일 생성
touch my_solution.py

# 자신의 풀이 작성
vim my_solution.py
```

### 3. 정답과 비교
정답은 각 단계 폴더의 `solutions.py`에 제공됩니다. **먼저 스스로 풀어본 후** 비교하세요.

### 4. 테스트 실행
```bash
python3 01-beginner/solutions.py      # 초급
python3 02-intermediate/solutions.py  # 중급
python3 03-advanced/solutions.py      # 고급 (실행 수 초 소요)
python3 04-expert/solutions.py        # 전문가 — 외부 라이브러리 없이 stdlib로 등가 구현
```

## 문제 풀이 팁

1. 🔍 **문제를 정확히 이해**: 입력/출력/제약조건 파악
2. 🧩 **작은 단위로 분해**: 큰 문제를 작은 함수로
3. 📝 **테스트 케이스 만들기**: 엣지 케이스 포함
4. 🐢 **점진적 개선**: 정답 → 효율 → 가독성
5. 🤔 **다른 방법 생각**: 같은 문제, 여러 풀이

## 난이도 표시

- ⭐ 매우 쉬움 (5-10분)
- ⭐⭐ 쉬움 (10-20분)
- ⭐⭐⭐ 보통 (20-40분)
- ⭐⭐⭐⭐ 어려움 (40-60분)
- ⭐⭐⭐⭐⭐ 매우 어려움 (1시간 이상)

## 진행 추적

각 문제 풀이 후 체크하세요:
- [ ] 문제 1. ...
- [ ] 문제 2. ...

## 막혔을 때

1. 챕터 다시 읽기
2. 작은 예제로 실험
3. 공식 문서 검색
4. Stack Overflow 검색
5. 정답 코드 참고 (마지막 수단)

## 🚀 도전 과제

기본 문제를 마쳤다면 도전 문제도 해보세요:
- LeetCode, HackerRank
- Project Euler
- Codewars
- Advent of Code
