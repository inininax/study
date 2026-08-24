"""
모니터링 (Monitoring)
======================

이 모듈에서 배울 내용:
1. 클라이언트 헬스 체크: is_ready / is_live / get_meta
2. REST 엔드포인트 직접 확인: ready, live, nodes
3. 클러스터 노드 통계: 객체 수, 샤드 상태
4. Prometheus 메트릭 연동
5. 백업/복원 기초

난이도: ⭐⭐⭐ (중간)
소요 시간: 1시간
"""

import weaviate
from weaviate.classes.config import Configure, Property, DataType

# requests: 프로젝트 requirements.txt에 포함된 HTTP 클라이언트
import requests


WEAVIATE_HTTP = "http://localhost:8080"
PROMETHEUS_PORT = 2114  # Weaviate 기본 메트릭 포트 (활성화 필요)


# ====================
# 0. 실습용 데이터 준비
# ====================


def setup_demo_collection(client: weaviate.WeaviateClient):
    """
    모니터링 관찰 대상이 될 작은 컬렉션 생성

    참고:
        - Vectorizer.none()으로 API 키 없이 실행 가능
        - 노드 통계의 object_count가 변하는 걸 눈으로 확인하기 위함
    """
    print("📦 데모 컬렉션 설정...")

    if client.collections.exists("MonitorDemo"):
        client.collections.delete("MonitorDemo")

    client.collections.create(
        name="MonitorDemo",
        properties=[
            Property(name="title", data_type=DataType.TEXT),
        ],
        vectorizer_config=Configure.Vectorizer.none(),
    )

    collection = client.collections.get("MonitorDemo")

    import random

    with collection.batch.dynamic() as batch:
        for i in range(10):
            batch.add_object(
                properties={"title": f"demo-{i}"},
                vector=[random.random() for _ in range(8)],
            )

    print("✅ MonitorDemo 컬렉션에 10개 객체 추가 완료\n")


# ====================
# 1. 클라이언트 헬스 체크
# ====================


def client_health_checks(client: weaviate.WeaviateClient):
    """
    클라이언트 API로 서비스 상태 확인

    참고:
        - is_ready(): 요청 처리 준비 완료? (배포 후 트래픽 받기 전 확인)
        - is_live(): 프로세스 살아있음? (쿠버네티스 liveness와 유사)
        - get_meta(): 버전, 활성 모듈 등 인스턴스 정보
        - 쿠버네티스 프로브 설계 시 readiness=/v1/.well-known/ready,
          liveness=/v1/.well-known/live 를 그대로 사용
    """
    print("\n" + "=" * 60)
    print("클라이언트 헬스 체크")
    print("=" * 60)

    print(f"\n🟢 is_ready(): {client.is_ready()}  ← 트래픽 받을 준비 됨?")
    print(f"🫀 is_live(): {client.is_live()}  ← 프로세스 살아있음?")

    meta = client.get_meta()
    print(f"\n🏷️ 버전: {meta.get('version')}")
    modules = meta.get("modules", {})
    print(f"🔌 활성 모듈: {', '.join(modules.keys()) if modules else '(없음)'}")


def rest_endpoint_checks():
    """
    HTTP 엔드포인트 직접 호출 (운영팀/스크립트 관점)

    참고:
        - GET /v1/.well-known/live   → 200이면 살아있음
        - GET /v1/.well-known/ready  → 200이면 준비됨
        - GET /v1/nodes              → 클러스터 노드 정보 (JSON)
        - 로드밸런서 헬스체크, 배치 스크립트 사전 점검 등에 그대로 활용
    """
    print("\n" + "=" * 60)
    print("REST 엔드포인트 직접 확인")
    print("=" * 60)

    endpoints = [
        ("/v1/.well-known/live", "liveness"),
        ("/v1/.well-known/ready", "readiness"),
        ("/v1/meta", "메타 정보"),
        ("/v1/nodes", "노드 정보"),
    ]

    for path, label in endpoints:
        try:
            response = requests.get(f"{WEAVIATE_HTTP}{path}", timeout=5)
            status_icon = "✅" if response.status_code == 200 else "⚠️"
            print(f"   {status_icon} GET {path} ({label}) → {response.status_code}")
        except requests.RequestException as e:
            print(f"   ❌ GET {path} ({label}) → 실패: {e}")


# ====================
# 2. 클러스터 노드 통계
# ====================


def cluster_statistics(client: weaviate.WeaviateClient):
    """
    클러스터/노드 통계 조회

    참고:
        - client.cluster.nodes(output="verbose"): 샤드별 통계까지 상세 조회
        - node.stats: 객체 수 / 샤드 수
        - shard.vector_indexing_status: 색인 진행 여부 (INDEXING 중이면 성능 주의)
        - 운영 대시보드의 '노드 현황' 패널 데이터 소스
    """
    print("\n" + "=" * 60)
    print("클러스터 노드 통계")
    print("=" * 60)

    nodes = client.cluster.nodes(output="verbose")

    for node in nodes:
        print(f"\n🖥️ 노드: {node.name}")
        print(f"   상태: {node.status} | 버전: {node.version}")
        print(f"   객체 수: {node.stats.object_count:,}개 | 샤드 수: {node.stats.shard_count}개")

        if node.shards:
            print("   샤드 목록:")
            for shard in node.shards[:5]:  # 너무 많으면 5개만
                print(
                    f"     - {shard.collection}/{shard.name}: "
                    f"{shard.object_count}개 객체, 색인={shard.vector_indexing_status}"
                )


# ====================
# 3. Prometheus 메트릭
# ====================


def prometheus_metrics_check():
    """
    Prometheus 메트릭 엔드포인트 확인

    참고:
        - Weaviate는 Prometheus 형식 메트릭 제공 (기본 포트 2114)
        - docker-compose.yml에 아래 환경 변수를 추가해야 활성화됨:

            PROMETHEUS_MONITORING_ENABLED: 'true'
            PROMETHEUS_MONITORING_PORT: '2114'
          ports에 "2114:2114" 노출도 필요

        - Grafana 대시보드 + Prometheus 스크레이핑이 표준 조합
    """
    print("\n" + "=" * 60)
    print("Prometheus 메트릭 확인")
    print("=" * 60)

    url = f"http://localhost:{PROMETHEUS_PORT}/metrics"

    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
    except requests.RequestException:
        print("\n⚠️ 메트릭 엔드포인트에 접속할 수 없습니다.")
        print("   → docker-compose.yml에 아래 설정을 추가한 뒤 재시작하세요:")
        print("      environment:")
        print("        PROMETHEUS_MONITORING_ENABLED: 'true'")
        print("        PROMETHEUS_MONITORING_PORT: '2114'")
        print("      ports:")
        print('        - "2114:2114"')
        return

    # 핵심 지표 몇 가지 추출해서 출력
    interesting = [
        "weaviate_objects_count",
        "weaviate_shards_count",
        "weaviate_queries_duration_seconds",
        "weaviate_batch_durations_seconds",
    ]

    print(f"\n📈 {url} 응답 예시:")
    found_any = False
    for line in response.text.splitlines():
        if any(line.startswith(metric) for metric in interesting):
            print(f"   {line}")
            found_any = True

    if not found_any:
        print("   (관심 지표가 아직 수집되지 않았습니다 - 쿼리를 더 실행해 보세요)")

    print("\n💡 이 파일을 Prometheus가 스크레이핑하면 Grafana로 시각화할 수 있습니다.")


# ====================
# 4. 백업 기초
# ====================


def backup_basics(client: weaviate.WeaviateClient):
    """
    백업 생성/상태 확인/복원 개념

    참고:
        - 백업 백엔드: filesystem(로컬), s3, gcs, azure
        - filesystem 백엔드를 쓰려면 docker-compose.yml 수정 필요:

            ENABLE_MODULES: 'text2vec-openai,generative-openai,backup-filesystem'
            BACKUP_FILESYSTEM_PATH: '/var/lib/weaviate/backups'
          volumes: 에 backups 디렉터리 마운트 추가

        - create(backup_id=..., backend=..., include_collections=[...])
        - restore 시 같은 이름 컬렉션이 있으면 실패 → 먼저 삭제 필요
        - 정기 백업 + 복원 리허설이 운영의 기본!
    """
    print("\n" + "=" * 60)
    print("백업 기초")
    print("=" * 60)

    from weaviate.classes.backup import BackupStorage

    backup_id = "monitor-demo-backup"

    print(f"\n💾 백업 시도: id='{backup_id}', backend=filesystem")

    try:
        result = client.backup.create(
            backup_id=backup_id,
            backend=BackupStorage.FILESYSTEM,
            include_collections=["MonitorDemo"],
            wait_for_completion=True,
        )
        print(f"   ✅ 백업 상태: {result.status}")

        # 생성 상태 폴링 (wait_for_completion=False일 때의 패턴)
        status = client.backup.get_create_status(
            backup_id=backup_id, backend=BackupStorage.FILESYSTEM
        )
        print(f"   📌 폴링 결과: {status.status}")

        # 복원은 '같은 이름 컬렉션이 없어야' 성공하므로 코드만 안내
        print("\n♻️ 복원 코드 예시 (실행하지 않음):")
        print(
            "   client.backup.restore(\n"
            "       backup_id='monitor-demo-backup',\n"
            "       backend=BackupStorage.FILESYSTEM,\n"
            "       wait_for_completion=True,\n"
            "   )"
        )

    except Exception as e:
        print(f"\n⚠️ 백업 실패: {type(e).__name__}")
        msg = str(e)
        print(f"   {msg[:150]}...")
        print("\n💡 원인 대부분: backup-filesystem 모듈 미활성화")
        print("   → docker-compose.yml에 다음을 추가하세요:")
        print("      ENABLE_MODULES: '...,backup-filesystem'")
        print("      BACKUP_FILESYSTEM_PATH: '/var/lib/weaviate/backups'")
        print("   (백업 코드 구조 자체는 동일하게 사용할 수 있습니다)")


# ====================
# 5. 메인 실행부
# ====================


def main():
    """메인 함수"""
    print("\n" + "📡" * 25)
    print("모니터링 (Monitoring) 학습")
    print("📡" * 25)

    try:
        with weaviate.connect_to_local() as client:
            # 0. 관찰 대상 준비
            setup_demo_collection(client)

            # 1. 클라이언트 헬스 체크
            client_health_checks(client)

            # 2. REST 엔드포인트 직접 확인
            rest_endpoint_checks()

            # 3. 클러스터 통계
            cluster_statistics(client)

            # 4. Prometheus 메트릭
            prometheus_metrics_check()

            # 5. 백업 기초
            backup_basics(client)

            # 실습 후 정리
            client.collections.delete("MonitorDemo")

    except Exception as e:
        print(f"\n❌ 에러 발생: {e}")
        import traceback

        traceback.print_exc()

    print("\n" + "🎉" * 25)
    print("학습 완료!")
    print("🎉" * 25)

    print("\n💡 핵심 정리:")
    print("   - ready(준비됨) vs live(살아있음)는 다른 개념!")
    print("   - /v1/.well-known/* 엔드포인트로 LB/K8s 헬스체크 구성")
    print("   - cluster.nodes()로 객체/샤드/색인 상태 감시")
    print("   - Prometheus(2114) + Grafana가 표준 모니터링 조합")
    print("   - 백업은 컬렉션 단위 + backup_id로 관리, 복원 리허설 필수")

    print("\n📚 다음 학습:")
    print("   project/ - 실전 프로젝트 (FastAPI 문서 검색 시스템)")


if __name__ == "__main__":
    main()


# ====================
# 학습 정리
# ====================

"""
🎓 학습 내용 정리:

1. 관찰 가능성(Observability) 3요소
   - 메트릭: Prometheus/Grafana (숫자로 보는 건강 상태)
   - 헬스체크: ready/live 엔드포인트 (살아있나? 준비됐나?)
   - 로그: LOG_LEVEL 조절, 구조화된 로깅

2. 헬스체크 엔드포인트
   - GET /v1/.well-known/ready  → readiness probe
   - GET /v1/.well-known/live   → liveness probe
   - 차이: ready는 샤드 로딩 등 '서빙 가능 여부' 반영

3. 백업 전략
   - filesystem: 개발/소규모, s3/gcs/azure: 운영 표준
   - backup_id로 관리, 증분 백업(incremental)도 지원
   - 복원 전제조건: 같은 이름 컬렉션 없어야 함

💡 실전 팁:
   - 배포 직후 is_ready() + 간단한 검색 스모크 테스트 자동화
   - object_count 급증/급감 알람 설정
   - vector_indexing_status가 INDEXING이면 쿼리 지연 가능 → 알람 고려

⚠️ 주의사항:
   - 메트릭 포트를 외부에 무단 노출하지 말 것 (내부망/보안 그룹 제한)
   - 백업 파일도 민감 데이터 포함 → 저장소 접근 권한 관리 필수

🔧 연습 과제:
   1. docker-compose.yml에 Prometheus 설정 추가하고 지표 확인하기
   2. backup-filesystem 모듈을 켜고 백업→컬렉션 삭제→복원 흐름 연습
   3. cluster.nodes() 출력을 JSON 파일로 덤프하는 스크립트 만들기
"""
