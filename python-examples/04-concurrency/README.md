# 04. Concurrency - 동시성 프로그래밍

> 💡 **Java/Go 개발자를 위한 핵심:**
> Python에는 **GIL(Global Interpreter Lock)**이 있어서 
> CPU 바운드 작업에서 멀티스레딩이 효과적이지 않습니다.
> I/O 바운드는 스레딩, CPU 바운드는 멀티프로세싱을 사용하세요.

## 🎯 학습 목표

1. GIL이 무엇이고 왜 존재하는지 이해
2. threading vs multiprocessing 사용 시점 구분
3. asyncio 패턴 습득
4. concurrent.futures 활용법

## 🔄 다른 언어와 비교

| 구분 | Java | Go | Python |
|------|------|-----|--------|
| 동시성 모델 | Thread | Goroutine | Thread / Process / Async |
| 병렬 실행 | ✅ 가능 | ✅ 가능 | ⚠️ GIL 제한 |
| 경량 스레드 | ❌ (Project Loom) | ✅ | ✅ asyncio |
| CPU 병렬 | 멀티스레드 | 멀티코어 | multiprocessing |

## ⚠️ 핵심 규칙

```
┌─────────────────────────────────────────────────────────┐
│  Python 동시성 선택 가이드                               │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  I/O 바운드 (네트워크, 파일, DB):                       │
│    → asyncio (권장) 또는 threading                      │
│                                                         │
│  CPU 바운드 (계산, 이미지 처리):                        │
│    → multiprocessing                                    │
│                                                         │
│  간단한 병렬화:                                         │
│    → concurrent.futures.ThreadPoolExecutor             │
│    → concurrent.futures.ProcessPoolExecutor            │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

## 📚 예제 목록

| 파일 | 설명 | 난이도 | 소요시간 |
|------|------|--------|----------|
| [01_gil_explained.py](./01_gil_explained.py) | GIL 이해 | ⭐⭐⭐ | 15분 |
| [04_asyncio_basics.py](./04_asyncio_basics.py) | asyncio 기초 | ⭐⭐ | 15분 |

## 🧭 확장 예정 주제

- 스레딩 기초
- 멀티프로세싱
- `concurrent.futures` 실무 패턴

## 🚀 실행 방법

```bash
python 01_gil_explained.py
```

## 📖 추가 학습 자료

- [asyncio 문서](https://docs.python.org/3/library/asyncio.html)
- [GIL 설명](https://realpython.com/python-gil/)
