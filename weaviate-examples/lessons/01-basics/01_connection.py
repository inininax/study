"""
Weaviate 연결 기초
===================

이 모듈에서 배울 내용:
1. Weaviate 클라이언트 생성 및 연결
2. 연결 상태 확인
3. Weaviate 메타데이터 조회
4. 리소스 관리 (연결 종료)

난이도: ⭐ (매우 쉬움)
소요 시간: 30분
"""

# ====================
# 1. 필요한 라이브러리 임포트
# ====================

import weaviate  # Weaviate Python 클라이언트
from weaviate.classes.init import Auth  # 인증 클래스 (필요시)
import os  # 환경 변수 접근용
from dotenv import load_dotenv  # .env 파일에서 환경 변수 로드

# 타입 힌트 (코드를 더 명확하게 만듭니다)
from typing import Dict, Any


# ====================
# 2. 환경 변수 로드
# ====================

# .env 파일에서 환경 변수를 로드합니다
# .env 파일에는 API 키, URL 등 민감한 정보를 저장합니다
load_dotenv()

# 환경 변수에서 Weaviate URL 가져오기
# os.getenv("키", "기본값"): 환경 변수가 없으면 기본값 사용
WEAVIATE_URL = os.getenv("WEAVIATE_URL", "http://localhost:8080")


# ====================
# 3. 연결 함수들
# ====================


def connect_to_weaviate_basic() -> weaviate.WeaviateClient:
    """
    Weaviate에 기본 연결 (로컬 인스턴스)

    Returns:
        weaviate.WeaviateClient: 연결된 클라이언트 객체

    참고:
        - 로컬에서 Docker로 실행 중인 Weaviate에 연결합니다
        - 인증이 필요 없는 개발 환경용입니다
    """
    print("🔌 Weaviate에 연결 중...")

    # 로컬 Weaviate 인스턴스에 연결
    # connect_to_local()은 http://localhost:8080에 자동으로 연결합니다
    client = weaviate.connect_to_local()

    print("✅ 연결 성공!")
    return client


def connect_to_weaviate_custom(url: str) -> weaviate.WeaviateClient:
    """
    Weaviate에 커스텀 URL로 연결

    Args:
        url: Weaviate 인스턴스 URL (예: "http://localhost:8080")

    Returns:
        weaviate.WeaviateClient: 연결된 클라이언트 객체

    예시:
        client = connect_to_weaviate_custom("http://my-weaviate.com")
    """
    print(f"🔌 Weaviate에 연결 중... (URL: {url})")

    # 커스텀 URL로 연결
    client = weaviate.connect_to_local(
        host=url.replace("http://", "").replace("https://", "").split(":")[0],
        port=int(url.split(":")[-1]) if ":" in url else 8080,
    )

    print("✅ 연결 성공!")
    return client


def check_connection_status(client: weaviate.WeaviateClient) -> Dict[str, Any]:
    """
    Weaviate 연결 상태 및 메타데이터 확인

    Args:
        client: Weaviate 클라이언트 객체

    Returns:
        Dict[str, Any]: 메타데이터 정보 (버전, 준비 상태 등)

    참고:
        - is_ready(): Weaviate가 요청을 받을 준비가 되었는지 확인
        - get_meta(): Weaviate 인스턴스의 상세 정보 조회
    """
    print("\n📊 연결 상태 확인 중...")

    # Weaviate가 준비되었는지 확인
    # 이는 health check와 유사합니다
    is_ready = client.is_ready()
    print(f"   준비 상태: {'✅ 준비됨' if is_ready else '❌ 준비되지 않음'}")

    # Weaviate 메타데이터 가져오기
    meta = client.get_meta()

    # 중요한 정보만 추출
    metadata = {
        "version": meta.get("version", "Unknown"),  # Weaviate 버전
        "hostname": meta.get("hostname", "Unknown"),  # 호스트 이름
    }

    print(f"   버전: {metadata['version']}")
    print(f"   호스트: {metadata['hostname']}")

    return metadata


# ====================
# 4. 실습 예제
# ====================


def example_basic_connection():
    """
    예제 1: 기본 연결 패턴

    이것이 가장 일반적인 패턴입니다!
    """
    print("\n" + "=" * 50)
    print("예제 1: 기본 연결")
    print("=" * 50)

    # 방법 1: 수동으로 연결 관리
    # 장점: 명시적
    # 단점: close()를 잊어버릴 수 있음
    client = None
    try:
        client = connect_to_weaviate_basic()
        check_connection_status(client)
    except Exception as e:
        print(f"❌ 에러 발생: {e}")
    finally:
        # finally 블록은 항상 실행됩니다 (에러가 나도 실행)
        if client:
            client.close()
            print("\n🔌 연결 종료")


def example_context_manager():
    """
    예제 2: 컨텍스트 매니저 사용 (권장!)

    with 문을 사용하면 자동으로 연결이 종료됩니다.
    이것이 Python의 Best Practice입니다!
    """
    print("\n" + "=" * 50)
    print("예제 2: 컨텍스트 매니저 (권장 방법)")
    print("=" * 50)

    # with 문을 사용하면 블록이 끝날 때 자동으로 close() 호출
    try:
        with weaviate.connect_to_local() as client:
            print("✅ Weaviate 연결 성공!")

            # 연결 상태 확인
            metadata = check_connection_status(client)

            # 추가 작업 수행 가능
            print("\n📋 상세 메타데이터:")
            print(f"   {metadata}")

        # with 블록이 끝나면 자동으로 client.close() 호출됨
        print("\n🔌 연결 자동 종료 완료")

    except Exception as e:
        print(f"❌ 에러 발생: {e}")
        print("\n💡 해결 방법:")
        print("   1. Docker에서 Weaviate가 실행 중인지 확인")
        print("   2. docker-compose up -d 명령 실행")
        print("   3. http://localhost:8080/v1/meta 접속 테스트")


def example_error_handling():
    """
    예제 3: 에러 처리

    실무에서는 항상 에러를 처리해야 합니다!
    """
    print("\n" + "=" * 50)
    print("예제 3: 에러 처리")
    print("=" * 50)

    try:
        # 잘못된 URL로 연결 시도
        with weaviate.connect_to_local(host="invalid-host") as client:
            client.is_ready()

    except weaviate.exceptions.WeaviateConnectionError as e:
        print(f"❌ 연결 에러: {e}")
        print("💡 Weaviate 서버가 실행 중인지 확인하세요")

    except Exception as e:
        print(f"❌ 예상치 못한 에러: {e}")


# ====================
# 5. 유틸리티 함수
# ====================


def create_client() -> weaviate.WeaviateClient:
    """
    재사용 가능한 클라이언트 생성 함수

    Returns:
        weaviate.WeaviateClient: 연결된 클라이언트

    참고:
        이 함수는 다른 모듈에서도 import해서 사용할 수 있습니다.
        예: from connection import create_client
    """
    return weaviate.connect_to_local()


# ====================
# 6. 메인 실행부
# ====================


def main():
    """
    메인 함수: 모든 예제를 순차적으로 실행합니다
    """
    print("\n" + "🚀" * 25)
    print("Weaviate 연결 학습 시작!")
    print("🚀" * 25)

    # 예제 1: 기본 연결
    example_basic_connection()

    # 예제 2: 컨텍스트 매니저 (권장)
    example_context_manager()

    # 예제 3: 에러 처리
    example_error_handling()

    print("\n" + "🎉" * 25)
    print("학습 완료!")
    print("🎉" * 25)

    print("\n📚 다음 학습:")
    print("   python 02_schema.py")


# Python 스크립트가 직접 실행될 때만 main() 호출
# 다른 파일에서 import 될 때는 실행되지 않음
if __name__ == "__main__":
    main()


# ====================
# 7. 학습 정리
# ====================

"""
🎓 학습 내용 정리:

1. Weaviate 클라이언트 연결
   - connect_to_local(): 로컬 인스턴스 연결
   - connect_to_weaviate_cloud(): 클라우드 연결 (필요시)

2. 연결 패턴
   - 수동 관리: try-finally 사용
   - 컨텍스트 매니저: with 문 사용 (권장!)

3. 연결 상태 확인
   - is_ready(): 준비 상태 확인
   - get_meta(): 메타데이터 조회

4. 에러 처리
   - try-except로 연결 에러 처리
   - 명확한 에러 메시지 제공

💡 실무 팁:
   - 항상 컨텍스트 매니저(with 문) 사용
   - 환경 변수로 설정 관리
   - 에러는 반드시 처리
   - 타입 힌트로 코드 명확성 향상

🔧 연습 과제:
   1. .env 파일에서 WEAVIATE_URL 변경해보기
   2. 에러 메시지를 의도적으로 발생시켜보기
   3. 다른 호스트/포트로 연결해보기
"""
