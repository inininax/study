# ex06 고급 매핑
## 상속 관계 매핑
### 요약
- 관계형 데이터베이스는 상속 관계 없음
- 슈퍼타입 서브타입 관계라는 모델링 기법이 객체 상속과 유사
- 상속관계 매핑: 객체의 상속과 구조와 DB의 슈퍼타입 서브타입 관계를 매핑
- 슈퍼타입 서브타입 논리 모델을 실제 물리 모델로 구현하는 방법
    - 각각 테이블로 변환 -> 조인 전략
    - 통합 테이블로 변환 -> 단일 테이블 전략
    - 서브타입 테이블로 변환 -> 구현 클래스마다 테이블 전략

### 주요 Annotation
- @Inheritance(strategy=InheritanceType.XXX)
    - InheritanceType.JOINED -> 조인 전략
    - InheritanceType.SINGLE_TABLE -> 단일 테이블 전략
    - InheritanceType.TABLE_PER_CLASS -> 구현 클래스마다 테이블 전략
- @DiscriminatorColumn(name=“DTYPE”) -> 부모(SINGLE_TABLE, TABLE_PER_CLASS 일 경우 자기 자신)의 DTYP의 컬럼명을 입력한다.
- @DiscriminatorValue(“XXX”) -> 상속받는 엔티티에 XXX값이 부모(SINGLE_TABLE, TABLE_PER_CLASS 일 경우 자기 자신)의 DTYP에 값을 입력한다.

```text
테이블 생성되는 예시
joined_item
    joined_album
    joined_book
    joined_movie

singletable_item

tableperclass_album
tableperclass_book
tableperclass_movie
```

### 조인 전략 JOINED
- 장점
    - 테이블 정규화
    - 외래 키 참조 무결성 제약조건 활용가능
    - 저장공간 효율화
- 단점
    - 조회 시 조인을 많이 사용, 성능 저하
    - 조회 쿼리가 복잡함
    - 데이터 저장 시 Insert SQL 2회 호출
  
### 단일 테이블 전략 SINGLE_TABLE
- 장점
    - 조인이 필요없고 일반적으로 조회 속도가 빠름
    - 조회 쿼리가 단순함
- 단점
    - 자식 엔티티가 매핑한 컬럼은 모두 null 허용
    - 단일 테이블에 모든 것을 저장하여 테이블의 컬럼이 많아지고 각 케이스별 사용 필드 구분이 직관적이지 않다.
    - 테이블이 너무 커질 경우 조회 성능이 안 나올 수 있다.

### 구현 클래스마다 테이블 전략 TABLE_PER_CLASS
- 실무에서 사용 안함
- 장점
    - 서브타입을 명확하게 구분해서 처리할 때 효율적
    - not null 제약 조건 사용 가능
- 단점
    - 여러 자식 테이블을 함께 조회할 때 성능이 느림 (UNION)
    - 자식 테이블을 통합해서 쿼리하기 어려움

---

## 공통 컬럼 상속 @MappedSuperclass
### 요약
- 상속관계 매핑 X
- 엔티티 X, 테이블과 매핑 X
- 부모 클래스를 상속 받는 자식 클래스에 매핑 정보만 제공
- 조회, 검색 불가 (em.find(BaseEntity) 불가)
- 직접 생성해서 사용할 일이 없으므로 추상 클래스 권장
- 테이블과 관계 없고, 단순히 엔티티가 공통으로 사용하는 매핑 정보를 모으는 역할
- 주로 등록일, 수정일, 등록자, 수정자 같은 전체 엔티티에서 공통 으로 적용하는 정보를 모을 때 사용
- 참고: @Entity 클래스는 엔티티나 @MappedSuperclass로 지 정한 클래스만 상속 가능