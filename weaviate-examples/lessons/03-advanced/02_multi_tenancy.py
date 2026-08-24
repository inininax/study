"""
멀티테넌시 (Multi-Tenancy)
===========================

이 모듈에서 배울 내용:
1. 멀티테넌트 컬렉션 생성
2. 테넌트 CRUD: 생성 / 조회 / 수정 / 삭제
3. 테넌트별 데이터 삽입과 조회 (격리 확인)
4. 자동 테넌트 생성/활성화 옵션
5. SaaS 아키텍처에서의 활용 패턴

난이도: ⭐⭐⭐⭐ (높음)
소요 시간: 1.5시간
"""

import weaviate
from weaviate.classes.config import Configure, Property, DataType
from weaviate.classes.tenants import Tenant, TenantActivityStatus


# ====================
# 1. 준비: 멀티테넌트 컬렉션 생성
# ====================


def setup_multi_tenant_collection(client: weaviate.WeaviateClient):
    """
    멀티테넌시가 활성화된 컬렉션 생성

    참고:
        - multi_tenancy_config=Configure.multi_tenancy(enabled=True)
        - 컬렉션 생성 시점에만 활성화 가능 (나중에 변경 불가!)
        - 각 테넌트는 독립 샤드로 저장 → 데이터 완전 격리
    """
    print("📦 멀티테넌트 프로젝트 컬렉션 설정...")

    if client.collections.exists("Project"):
        client.collections.delete("Project")

    client.collections.create(
        name="Project",
        properties=[
            Property(name="name", data_type=DataType.TEXT),
            Property(name="description", data_type=DataType.TEXT),
            Property(name="status", data_type=DataType.TEXT),
        ],
        vectorizer_config=Configure.Vectorizer.text2vec_openai(
            model="text-embedding-3-small"
        ),
        # ★ 핵심: 멀티테넌시 활성화
        multi_tenancy_config=Configure.multi_tenancy(
            enabled=True,
            auto_tenant_creation=False,  # 존재하지 않는 테넌트 자동 생성 여부
            auto_tenant_activation=False,  # 비활성 테넌트 자동 활성화 여부
        ),
    )

    print("✅ Project 컬렉션 생성 완료 (multi-tenancy enabled)\n")


# ====================
# 2. 테넌트 CRUD
# ====================


def tenant_crud(client: weaviate.WeaviateClient):
    """
    테넌트 생명주기 관리

    참고:
        - tenants.create(): 테넌트(샤드) 생성
        - tenants.get(): 전체 테넌트 목록과 상태 조회
        - tenants.update(): 테넌트 상태 변경
        - tenants.remove(): 테넌트 삭제 (데이터도 함께 삭제!)
        - Tenant(name="...")로 테넌트 객체 정의
    """
    print("\n" + "=" * 60)
    print("테넌트 CRUD")
    print("=" * 60)

    projects = client.collections.get("Project")

    # Create: 테넌트 3개 생성
    print("\n➕ 테넌트 생성: team-alpine, team-brix, team-cove")
    projects.tenants.create(
        [
            Tenant(name="team-alpine"),
            Tenant(name="team-brix"),
            Tenant(name="team-cove"),
        ]
    )
    print("   ✅ 3개 테넌트 생성 완료")

    # Read: 테넌트 목록 조회
    print("\n📋 테넌트 목록:")
    tenants = projects.tenants.get()
    for name, tenant in sorted(tenants.items()):
        print(f"   - {name}: {tenant.activity_status}")

    # Update: 테넌트 비활성화 (사용 중이 아닌 고객의 리소스 절약)
    print("\n🔄 team-cove 비활성화 (INACTIVE)")
    projects.tenants.update(
        [Tenant(name="team-cove", activity_status=TenantActivityStatus.INACTIVE)]
    )
    tenants = projects.tenants.get()
    for name in ("team-alpine", "team-brix", "team-cove"):
        status = tenants[name].activity_status if name in tenants else "NOT FOUND"
        print(f"   - {name}: {status}")

    return tenants


def insert_and_query_per_tenant(client: weaviate.WeaviateClient):
    """
    테넌트별 데이터 삽입/조회 + 격리 확인

    참고:
        - collection.with_tenant("테넌트명")으로 테넌트 스코프 획득
        - 같은 컬렉션이지만 테넌트가 다르면 서로 데이터를 못 봄!
        - 모든 작업(insert/query/search/aggregate)은 with_tenant와 함께
    """
    print("\n" + "=" * 60)
    print("테넌트별 데이터 격리 확인")
    print("=" * 60)

    projects = client.collections.get("Project")

    # 테넌트별 데이터 삽입
    sample_data = {
        "team-alpine": [
            {"name": "알파인 검색엔진", "description": "산악 커뮤니티용 검색 서비스", "status": "active"},
            {"name": "알파인 추천", "description": "등산 코스 추천 시스템", "status": "beta"},
        ],
        "team-brix": [
            {"name": "브릭스 챗봇", "description": "건자재 B2B 문의 챗봇", "status": "active"},
        ],
    }

    print("\n➕ 테넌트별 데이터 삽입:")
    for tenant_name, items in sample_data.items():
        scoped = projects.with_tenant(tenant_name)
        for item in items:
            scoped.data.insert(properties=item)
        print(f"   - {tenant_name}: {len(items)}개 삽입")

    # 테넌트별 조회
    print("\n📋 테넌트별 데이터 조회:")
    for tenant_name in ("team-alpine", "team-brix"):
        scoped = projects.with_tenant(tenant_name)
        response = scoped.query.fetch_objects(limit=10)
        names = [obj.properties["name"] for obj in response.objects]
        print(f"   - {tenant_name}: {names}")

    # ★ 격리 핵심 증명: team-alpine 스코프에서 team-brix 데이터 검색 시도
    print("\n🔒 데이터 격리 증명:")
    alpine = projects.with_tenant("team-alpine")
    response = alpine.query.near_text(query="챗봇", limit=10)  # brix의 '챗봇'을 찾아도...
    found = [obj.properties["name"] for obj in response.objects]
    print(f"   team-alpine에서 '챗봇' 검색 결과: {found or '(없음!)'}")
    print("   → 다른 테넌트(team-brix)의 데이터는 절대 보이지 않음 ✅")


def auto_tenant_demo(client: weaviate.WeaviateClient):
    """
    자동 테넌트 생성/활성화 옵션 데모

    참고:
        - auto_tenant_creation=True: 없는 테넌트에 insert하면 자동 생성
          (신규 가입 고객 처리에 유용)
        - auto_tenant_activation=True: INACTIVE 테넌트에 요청이 오면
          자동으로 활성화 후 처리
        - Weaviate 1.26 기준 지원
    """
    print("\n" + "=" * 60)
    print("자동 테넌트 생성 데모")
    print("=" * 60)

    if client.collections.exists("AutoTenantDoc"):
        client.collections.delete("AutoTenantDoc")

    client.collections.create(
        name="AutoTenantDoc",
        properties=[
            Property(name="content", data_type=DataType.TEXT),
        ],
        vectorizer_config=Configure.Vectorizer.none(),  # 벡터 직접 제공 (키 불필요)
        multi_tenancy_config=Configure.multi_tenancy(
            enabled=True,
            auto_tenant_creation=True,  # ★ 자동 생성 켜기
            auto_tenant_activation=True,
        ),
    )

    docs = client.collections.get("AutoTenantDoc")

    # 'new-team'이라는 테넌트는 아직 없지만 바로 insert!
    import random

    vector = [random.random() for _ in range(8)]  # Vectorizer.none()이라 벡터 필수

    print("\n➕ 존재하지 않는 테넌트 'new-team'에 곧바로 삽입...")
    docs.with_tenant("new-team").data.insert(
        properties={"content": "자동 생성된 테넌트의 첫 문서"},
        vector=vector,
    )
    print("   ✅ 성공! (auto_tenant_creation=True 덕분)")

    tenants = docs.tenants.get()
    for name, tenant in tenants.items():
        print(f"   - 확인: {name} ({tenant.activity_status})")

    # 정리
    client.collections.delete("AutoTenantDoc")


def query_inactive_tenant_error(client: weaviate.WeaviateClient):
    """
    비활성(INACTIVE) 테넌트 접근 시 에러 처리

    참고:
        - INACTIVE 테넌트는 샤드가 언로드되어 쿼리할 수 없음
        - 실무에서는 이런 에러를 받으면 activate 후 재시도하는 패턴 사용
    """
    print("\n" + "=" * 60)
    print("비활성 테넌트 에러 처리")
    print("=" * 60)

    projects = client.collections.get("Project")

    # team-cove는 앞서 INACTIVE로 만들어 둠
    try:
        cove = projects.with_tenant("team-cove")
        cove.query.fetch_objects(limit=5)
        print("   (예상과 다름: 비활성 테넌트에서 조회됨)")

    except Exception as e:
        print(f"\n⚠️ 예상대로 실패: {type(e).__name__}")
        print(f"   메시지: {str(e)[:100]}...")

    # 복구 패턴: 활성화 후 재시도
    print("\n🔧 활성화 후 재시도:")
    projects.tenants.activate("team-cove")
    cove = projects.with_tenant("team-cove")
    response = cove.query.fetch_objects(limit=5)
    print(f"   ✅ team-cove 활성화 → 조회 성공 ({len(response.objects)}개 객체)")


def cleanup_tenants(client: weaviate.WeaviateClient):
    """테넌트 삭제 실습"""
    print("\n" + "=" * 60)
    print("정리: 테넌트 삭제")
    print("=" * 60)

    projects = client.collections.get("Project")
    projects.tenants.remove(["team-alpine", "team-brix", "team-cove"])

    remaining = projects.tenants.get()
    print(f"\n🗑️ 삭제 후 남은 테넌트: {list(remaining.keys()) or '(없음)'}")


# ====================
# 6. 메인 실행부
# ====================


def main():
    """메인 함수"""
    print("\n" + "🏢" * 25)
    print("멀티테넌시 (Multi-Tenancy) 학습")
    print("🏢" * 25)

    try:
        with weaviate.connect_to_local() as client:
            # 1. 준비
            setup_multi_tenant_collection(client)

            # 2. 테넌트 CRUD
            tenant_crud(client)

            # 3. 테넌트별 삽입/조회 + 격리 확인
            insert_and_query_per_tenant(client)

            # 4. 비활성 테넌트 에러 처리
            query_inactive_tenant_error(client)

            # 5. 자동 테넌트 생성
            auto_tenant_demo(client)

            # 6. 정리
            cleanup_tenants(client)

    except Exception as e:
        print(f"\n❌ 에러 발생: {e}")
        import traceback

        traceback.print_exc()

    print("\n" + "🎉" * 25)
    print("학습 완료!")
    print("🎉" * 25)

    print("\n💡 핵심 정리:")
    print("   - multi_tenancy_config로 컬렉션 단위 활성화 (생성 시에만!)")
    print("   - with_tenant()로 모든 작업의 테넌트 스코프 지정")
    print("   - 테넌트 = 독립 샤드 → 데이터 완전 격리 + 리소스 절약")
    print("   - INACTIVE 테넌트는 언로드되어 쿼리 불가 (activate로 복구)")

    print("\n📚 다음 학습:")
    print("   python 03_performance_optimization.py")


if __name__ == "__main__":
    main()


# ====================
# 학습 정리
# ====================

"""
🎓 학습 내용 정리:

1. 멀티테넌시 설정
   - enabled: 기능 on/off (컬렉션 생성 시에만 결정)
   - auto_tenant_creation: insert 시 테넌트 자동 생성
   - auto_tenant_activation: 요청 시 자동 활성화

2. 테넌트 운영 API
   - create / get / update / remove / exists
   - activate / deactivate: 샤드 로드/언로드 (비용 절감)
   - activity_status: ACTIVE / INACTIVE / OFFLOADED 등

3. SaaS 설계 패턴
   - 고객사 = 테넌트: 한 컬렉션으로 수천 고객 처리
   - 신규 가입: auto creation으로 무중단 온보딩
   - 휴면 고객: INACTIVE 전환으로 메모리 절약

💡 실전 팁:
   - 테넌트 이름은 URL 슬러그처럼 소문자-하이픈 권장
   - 테넌트 수백 개까지는 자유롭게, 수만 개면 오프로딩(OFFLOADED) 검토
   - with_tenant를 빠뜨리면 에러가 나므로(멀티테넌트 컬렉션은 필수)
     애플리케이션 라우터에서 미들웨어로 주입하는 것이 안전

⚠️ 주의사항:
   - tenants.remove()는 해당 테넌트 데이터를 영구 삭제!
   - 멀티테넌트 컬렉션은 일반 컬렉션으로 되돌릴 수 없음
   - 테넌트 간 교차 검색은 불가능 (설계상 격리 보장)

🔧 연습 과제:
   1. 테넌트별 aggregate.over_all로 객체 수 비교하기
   2. deactivate → activate 사이클 타이밍 재보기
   3. auto_tenant_activation=False일 때 에러 메시지 비교해보기
"""
