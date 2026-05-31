# ex01 hello jpa
## 개념
### 영속성 컨텍스트
- 엔티티 매니저 팩토리와 엔티티 매니저
- JPA에서 말하는 1차 캐시에 엔티티를 저장 (EntityManager.persist(entity) 등)

### 엔티티 생명주기
- 비영속 (new/transient): 영속성 컨텍스트와 전혀 관계 없는 상태
- 영속 (managed): 영속성 컨텍스트에 관리되는 상태
- 준영속 (detached): 영속성 컨텍스트에 저장되었다가 분리된 상태
- 삭제 (removed): 삭제된 상태

### 영속성 컨텍스트의 이점
- 1차 캐시
- 동일성 보장 (identity)
    - find 시 1차 캐시 내에 저장 후 응답하여 동일 항목 조회 시 모든 엔티티가 동일성 보장
    - 단 detach, clear, close을 할 경우 제외
- 트랜잭션을 지원하는 쓰기 지연 (Transactional write-behind)
    - 1차 캐시에서 쓰기 지연을 자동으로 해주기 때문에 편리함
    - 옵션 설정만으로 batch 처리 가능
- 변경 감지 (Dirty checking)
    - 1차 캐시에서 flush가 이뤄지는 시점에 엔티티를 비교
- 지연 로딩 (Lazy loading)

### 플러시
- 변경 감지
- 수정된 엔티티 쓰기 지연 sql 저장소에 등록
- 쓰기 지연 sql 저장소의 쿼리를 데이터베이스에 전송
- 영속성 컨텍스트를 비우지 않음
- 영속성 컨텍스트의 변경 내용을 데이터베이스에 동기화
- 트랜잭션이라는 작업 단위가 중요 (커밋 직전에만 동기화)

### 준영속 상태
- 영속 -> 준영속
- 영속 상태의 엔티티가 영속성 컨텍스트에서 분리
- 영속성 컨텍스트가 제공하는 기능을 사용 못함
- em.detach(entity): 특정 엔티티만 준영속 상태로 전환
- em.clear(): 영속성 컨텍스트를 완전히 초기화
- em.close(): 영속성 컨텍스트를 종료

### 데이터베이스 스키마 자동 생성 (hibernate.hbm2ddl.auto)
- 개발 초기 (운영 서버에서 사용 절대 금지)
    - create: 기존테이블 삭제 후 다시 생성 (DROP + CREATE)
    - create-drop: create와 같으나 종료시점에 테이블 DROP
    - update: 없을 경우 생성, 변경분만 반영, unique 등 일부 속성은 변경되지 않음 (Alter 잘못 사용 시 table lock 발생, 운영 DB에는 사용하면 안됨)
- 스테이징, 운영 서버
    - validate: 엔티티와 테이블이 정상 매핑되었는지만 확인
    - none: 사용하지 않음

### @Id, @GeneratedValue
- 작성 중...(@GeneratedValue 추가 시 sql 실행 위치가 변경 됨, 테스트 중)

### 기본 Annotation
- @Id 
- @GeneratedValue
- @Column
- @Enumerated(EnumType.STRING) private [Enum] xxx;
- @Temporal(TemporalType.TIMESTAMP) private Date xxx;
- private LocalDateTime xxx; : LocalDate, LocalDateTime은 별도 Annotation 불필요
- @Lob private String xxx;
- @Transient private int temp; : table column과 관련없는 property
