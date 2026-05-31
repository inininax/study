"""
01_gil_explained.py - GIL (Global Interpreter Lock) 이해

📌 핵심 개념:
    GIL은 CPython 인터프리터의 뮤텍스로, 한 번에 하나의 스레드만 
    Python 바이트코드를 실행할 수 있게 합니다.

🔄 다른 언어 비교:
    - Java: GIL 없음, 진정한 병렬 실행
    - Go: GIL 없음, goroutine으로 병렬 실행
    - Python: GIL로 인해 CPU 바운드에서 병렬 제한

⚠️ 주의사항:
    - CPU 바운드: 멀티스레딩 비효율 → multiprocessing 사용
    - I/O 바운드: 멀티스레딩 효과적

📚 참고: https://wiki.python.org/moin/GlobalInterpreterLock
"""

from __future__ import annotations

import threading
import multiprocessing
import time
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor


def cpu_bound_task(n: int) -> int:
    """CPU 집약적 작업 (피보나치)."""
    if n < 2:
        return n
    a, b = 0, 1
    for _ in range(n - 1):
        a, b = b, a + b
    return b


def io_bound_task(seconds: float) -> str:
    """I/O 바운드 작업 시뮬레이션."""
    time.sleep(seconds)
    return f"Slept for {seconds}s"


def sequential_cpu_demo() -> None:
    """순차 실행 (CPU 바운드)."""
    print("\n📌 CPU 바운드: 순차 실행")
    print("-" * 50)
    
    start = time.perf_counter()
    results = [cpu_bound_task(100000) for _ in range(4)]
    elapsed = time.perf_counter() - start
    
    print(f"  소요 시간: {elapsed:.2f}초")


def threaded_cpu_demo() -> None:
    """멀티스레딩 (CPU 바운드) - GIL로 인해 느림!"""
    print("\n📌 CPU 바운드: 멀티스레딩 (GIL 영향)")
    print("-" * 50)
    
    start = time.perf_counter()
    
    with ThreadPoolExecutor(max_workers=4) as executor:
        results = list(executor.map(cpu_bound_task, [100000] * 4))
    
    elapsed = time.perf_counter() - start
    print(f"  소요 시간: {elapsed:.2f}초")
    print("  ⚠️ 순차 실행과 비슷하거나 더 느림!")


def multiprocess_cpu_demo() -> None:
    """멀티프로세싱 (CPU 바운드) - 진정한 병렬!"""
    print("\n📌 CPU 바운드: 멀티프로세싱 (GIL 우회)")
    print("-" * 50)
    
    start = time.perf_counter()
    
    with ProcessPoolExecutor(max_workers=4) as executor:
        results = list(executor.map(cpu_bound_task, [100000] * 4))
    
    elapsed = time.perf_counter() - start
    print(f"  소요 시간: {elapsed:.2f}초")
    print("  ✅ 실제 병렬 실행으로 빠름!")


def threaded_io_demo() -> None:
    """멀티스레딩 (I/O 바운드) - 효과적!"""
    print("\n📌 I/O 바운드: 멀티스레딩")
    print("-" * 50)
    
    # 순차 실행
    start = time.perf_counter()
    for _ in range(4):
        io_bound_task(0.5)
    sequential_time = time.perf_counter() - start
    print(f"  순차 실행: {sequential_time:.2f}초")
    
    # 멀티스레딩
    start = time.perf_counter()
    with ThreadPoolExecutor(max_workers=4) as executor:
        results = list(executor.map(io_bound_task, [0.5] * 4))
    threaded_time = time.perf_counter() - start
    print(f"  멀티스레딩: {threaded_time:.2f}초")
    print(f"  ✅ {sequential_time/threaded_time:.1f}배 빠름!")


def summary() -> None:
    """GIL 요약."""
    print("""
    ╔═══════════════════════════════════════════════════════════════╗
    ║                      GIL 정리                                  ║
    ╠═══════════════════════════════════════════════════════════════╣
    ║                                                               ║
    ║  GIL (Global Interpreter Lock):                               ║
    ║    - CPython의 메모리 관리를 단순화하기 위한 뮤텍스           ║
    ║    - 한 번에 하나의 스레드만 Python 코드 실행                 ║
    ║                                                               ║
    ║  CPU 바운드 (계산 집약):                                      ║
    ║    - 멀티스레딩 ❌ (GIL로 인해 병렬 불가)                      ║
    ║    - 멀티프로세싱 ✅ (각 프로세스에 별도 GIL)                  ║
    ║                                                               ║
    ║  I/O 바운드 (네트워크, 파일):                                 ║
    ║    - 멀티스레딩 ✅ (I/O 대기 중 GIL 해제)                      ║
    ║    - asyncio ✅ (더 효율적)                                    ║
    ║                                                               ║
    ║  💡 Python 3.13+에서 GIL 비활성화 옵션 추가 예정!              ║
    ║                                                               ║
    ╚═══════════════════════════════════════════════════════════════╝
    """)


def main() -> None:
    """메인 실행."""
    print("=" * 60)
    print("🔒 GIL (Global Interpreter Lock) 이해")
    print("=" * 60)
    
    sequential_cpu_demo()
    threaded_cpu_demo()
    multiprocess_cpu_demo()
    threaded_io_demo()
    summary()


if __name__ == "__main__":
    main()

