# 03. Memory and GC - 메모리 관리 & 가비지 컬렉션

> 💡 **Java/Go 개발자를 위한 핵심:**
> Python(CPython)은 **참조 카운팅 + 순환 GC**로 메모리를 관리합니다.
> JVM의 Mark & Sweep이나 Go의 Concurrent GC와는 다른 방식입니다.

## 🎯 학습 목표

1. CPython의 참조 카운팅 이해
2. 순환 GC 동작 방식 이해
3. 메모리 프로파일링 방법 습득
4. __slots__를 통한 최적화

## 🔄 다른 언어와 비교

| 구분 | Java (JVM) | Go | Python (CPython) |
|------|------------|-----|------------------|
| GC 방식 | Mark & Sweep (세대별) | Concurrent Mark & Sweep | 참조 카운팅 + 순환 GC |
| 해제 시점 | 지연 (GC 실행 시) | 지연 (GC 실행 시) | 즉시 (참조 0) + 지연 |
| GC 일시정지 | 있음 (STW) | 최소화 | 거의 없음 |
| 순환 참조 | 자동 처리 | 자동 처리 | 순환 GC로 처리 |

## 📚 예제 목록

| 파일 | 설명 | 난이도 | 소요시간 |
|------|------|--------|----------|
| [01_reference_counting.py](./01_reference_counting.py) | 참조 카운팅 동작 | ⭐⭐ | 10분 |

## 🧭 확장 예정 주제

- gc 모듈 활용
- 메모리 프로파일링
- `__slots__` 최적화

## 🚀 실행 방법

```bash
# 메모리 프로파일러 설치 (선택)
pip install memory-profiler

# 예제 실행
python 01_reference_counting.py
```

## 📖 추가 학습 자료

- [gc 모듈 문서](https://docs.python.org/3/library/gc.html)
- [tracemalloc 문서](https://docs.python.org/3/library/tracemalloc.html)
