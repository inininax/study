"""
04_asyncio_basics.py - asyncio 기초

📌 핵심 개념:
    asyncio는 async/await 문법을 사용하는 비동기 프로그래밍 프레임워크입니다.
    단일 스레드에서 I/O 작업을 효율적으로 처리합니다.

🔄 다른 언어 비교:
    - Go: goroutine (런타임이 스케줄링)
    - Java: CompletableFuture, Project Loom (Virtual Threads)
    - JavaScript: Promise, async/await
    - Python: asyncio, async/await

📚 참고: https://docs.python.org/3/library/asyncio.html
"""

from __future__ import annotations

import asyncio
import time


async def fetch_data(name: str, delay: float) -> str:
    """비동기 데이터 가져오기 시뮬레이션."""
    print(f"  {name}: 요청 시작")
    await asyncio.sleep(delay)  # I/O 대기 시뮬레이션
    print(f"  {name}: 완료 ({delay}초)")
    return f"{name} 데이터"


async def basic_async_demo() -> None:
    """기본 async/await 사용법."""
    print("\n📌 기본 async/await")
    print("-" * 50)
    
    start = time.perf_counter()
    
    # 순차 실행
    result1 = await fetch_data("Task1", 1)
    result2 = await fetch_data("Task2", 1)
    
    elapsed = time.perf_counter() - start
    print(f"\n  순차 실행 소요 시간: {elapsed:.2f}초")


async def concurrent_async_demo() -> None:
    """동시 실행 (asyncio.gather)."""
    print("\n📌 동시 실행 (asyncio.gather)")
    print("-" * 50)
    
    start = time.perf_counter()
    
    # 동시 실행
    results = await asyncio.gather(
        fetch_data("Task1", 1),
        fetch_data("Task2", 1),
        fetch_data("Task3", 1),
    )
    
    elapsed = time.perf_counter() - start
    print(f"\n  동시 실행 소요 시간: {elapsed:.2f}초")
    print(f"  결과: {results}")


async def task_demo() -> None:
    """Task로 백그라운드 실행."""
    print("\n📌 Task 생성")
    print("-" * 50)
    
    async def background_task(name: str) -> None:
        for i in range(3):
            print(f"  {name}: 작업 {i+1}")
            await asyncio.sleep(0.3)
    
    # Task 생성 (즉시 시작)
    task1 = asyncio.create_task(background_task("BG1"))
    task2 = asyncio.create_task(background_task("BG2"))
    
    print("  메인: 다른 작업 수행 중...")
    await asyncio.sleep(0.5)
    
    # Task 완료 대기
    await task1
    await task2
    print("  모든 Task 완료")


async def timeout_demo() -> None:
    """타임아웃 처리."""
    print("\n📌 타임아웃 처리")
    print("-" * 50)
    
    async def slow_task() -> str:
        await asyncio.sleep(5)
        return "완료"
    
    try:
        # 1초 타임아웃
        result = await asyncio.wait_for(slow_task(), timeout=1.0)
        print(f"  결과: {result}")
    except asyncio.TimeoutError:
        print("  ⚠️ 타임아웃 발생!")


async def exception_handling_demo() -> None:
    """예외 처리."""
    print("\n📌 예외 처리")
    print("-" * 50)
    
    async def may_fail(should_fail: bool) -> str:
        await asyncio.sleep(0.1)
        if should_fail:
            raise ValueError("의도적 실패")
        return "성공"
    
    # gather with return_exceptions
    results = await asyncio.gather(
        may_fail(False),
        may_fail(True),
        may_fail(False),
        return_exceptions=True  # 예외를 결과로 반환
    )
    
    for i, result in enumerate(results):
        if isinstance(result, Exception):
            print(f"  Task {i}: 예외 - {result}")
        else:
            print(f"  Task {i}: {result}")


def main() -> None:
    """메인 실행."""
    print("=" * 60)
    print("⚡ asyncio 기초")
    print("=" * 60)
    
    # 이벤트 루프 실행
    asyncio.run(basic_async_demo())
    asyncio.run(concurrent_async_demo())
    asyncio.run(task_demo())
    asyncio.run(timeout_demo())
    asyncio.run(exception_handling_demo())
    
    print("""
    ╔═══════════════════════════════════════════════════════════════╗
    ║                    asyncio 정리                                ║
    ╠═══════════════════════════════════════════════════════════════╣
    ║                                                               ║
    ║  핵심 개념:                                                   ║
    ║    - async def: 코루틴 함수 정의                              ║
    ║    - await: 코루틴 실행 및 대기                               ║
    ║    - asyncio.run(): 이벤트 루프 실행                          ║
    ║                                                               ║
    ║  동시 실행:                                                   ║
    ║    - asyncio.gather(): 여러 코루틴 동시 실행                  ║
    ║    - asyncio.create_task(): 백그라운드 실행                   ║
    ║    - asyncio.wait_for(): 타임아웃 설정                        ║
    ║                                                               ║
    ║  💡 Go goroutine vs Python asyncio:                           ║
    ║    - goroutine: 런타임이 자동 스케줄링                        ║
    ║    - asyncio: await 지점에서만 스위칭                         ║
    ║                                                               ║
    ╚═══════════════════════════════════════════════════════════════╝
    """)


if __name__ == "__main__":
    main()

