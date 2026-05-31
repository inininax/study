# ex04 다양한 연관관계 매핑
## 개념
- 연관관계 매핑 시 고려사항 3가지
    - 다중성
    - 단방향, 양방향 (하단 참고)
    - 연관관계의 주인
- 다대일 (N:1): @ManyToOne
- 일대다 (1:N): @OneToMany(mappedBy = "참조할 객체의 필드명")
- 일대일 (1:1): @OneToOne
- 다대다 (N:M): @ManyToMany

## 단방향, 양방향
- 테이블
    - 외래 키 하나로 양쪽 조인 가능
    - 테이블은 방향이라는 개념이 없음
- 객체
    - 참조용 필드가 있는 쪽으로만 참조 가능
    - 한쪽만 참조하면 단방향
    - 양쪽이 서로 참조하면 양방향
    
## 연관관계의 주인
- 테이블은 외래 키 하나로 두 테이블이 연관 관계를 맺음
- 객체 양방향 관계는 A->B, B->A 처럼 참조가 2군데
- 객체 양방향 관계는 참조가 2군데 있음, 둘중 주인은 테이블의 외래 키를 관리할 곳으로 지정한다.
- 연관관계의 주인: 외래 키를 관리하는 참조
- 주인의 반대편: 외래 키에 영향을 주지 않음, 단순 조회만 가능

## 다대일 (N:1)
- @ManyToOne
- Members(N, Owner) : Team(1)
- 외래 키가 있는 쪽이 연관관계의 주인 (예제에서는 Member가 Owner)
  
## 일대다 (1:N)
- @OneToMany(mappedBy = "참조할 객체의 필드명")
- 일대다 단방향은 일대다(1:N)에서 일(1)이 연관관계의 주인 (예제에서는 Team이 Owner)
- 테이블 일대다 관계는 항상 다(N) 쪽에 외래 키가 있다.
- 객체와 테이블의 차이 때문에 반대편 테이블의 외래 키를 관리하는 특이한 구조이다.
- @JoinColumn을 꼭 사용해야한다.<br>
  그렇지 않으면 조인 테이블 방식을 사용한다. (중간에 테이블을 하나 추가)<br>
  (예시: @JoinColumn을 사용하지 않으면 team_member 테이블이 추가 생성됨)
- 일대다 단방향 매핑의 단점
    - 엔티티가 관리하는 외래 키가 다른 테이블에 있음 (다대일과 비교하여 특이점)
    - 연관관계 관리를 위해 추가로 UPDATE SQL 실행
    - 일대다 단방향 매피 보다는 다대일 양방향 매핑을 사용한다.
- 일대다 양방향 정리
    - 이런 매핑은 공식적으로 없다. (다대일의 반대이기 때문)
    - 읽기 전용 필드 전략 (아래 예시 참고) -> @JoinColumn(insertable = false, updatable = false)
    - 읽기 전용 필드를 사용해서 양방향 처럼 사용하는 방법
    - 일대다 단방향 매피 보다는 다대일 양방향 매핑을 사용한다.
```text
public class OneToManyTeam {
    ...생략...

    // OneToManyTeam이 Owner로 OneToManyTeam에 의해 team_id 생성됨
    @OneToMany
    @JoinColumn(name = "team_id")
    private List<OneToManyMember> members = new ArrayList<>();
}

public class OneToManyMember {
    ...생략...

    // OneToManyTeam이 Owner로 OneToManyTeam에 의해 team_id 생성됨
    @ManyToOne
    @JoinColumn(name = "team_id", insertable = false, updatable = false) // 양방향 사용 시 - 읽기 전용으로 설정
    private OneToManyTeam team;
}
```

## 일대일 (1:1)
- @OneToOne
- 그 반대도 일대일 (말 그대로 어느쪽으로 FK를 설정해도 무관하다는 뜻)
- 주 테이블이나 대상 테이블 중 외래 키를 선택 가능
- 외래 키에 데이터베이스 유니크(UNI) 제약 조건 추가
- 외래 키가 있는 곳이 연관관계의 주인, 반대편은 mappedBy 적용
- 주 테이블에 외래 키
    - 주 객체가 대상 객체의 참조를 가지는 것 처럼 주 테이블에 외래 키를 두고 대상 테이블을 찾음
    - JPA 매핑 관리
    - 객체 지향 개발자들이 선호
    - 장점: 주테이블만 조회해도 대상 테이블의 데이터 존재 여부 확인 가능
    - 단점: 값이 없으면 외래 키에 null 허용 (치명적)
- 대상 테이블에 외래 키
    - 대상 테이블에 외래 키가 존재
    - 전통적인 데이터베이스 개발자가 선호
    - 장점: 주 테이블과 대상 테이블을 일대일에서 일대다 관계로 변경 시 테이블 구조 유지됨
    - 단점: 프록시 기능의 한계로 지연 로딩으로 설정해도 항상 즉시 로딩됨 (치명적), 값이 있는지 없는지 모르기 때문에 항상 select 하기 때문에 프록시로 만드는 의미가 없음.

## 다대다 (N:M)
- @ManyToMany
- @JoinTable로 연결 테이블 지정
- 데이터베이스에서는 다대다 관계를 표현할 수 없음 (객체에서 컬렉션을 사용해 구현 가능)
- 객체는 컬렉션을 사용해서 객체 2개로 다대다 관계 가능
- 두 테이블간 중간 테이블이 생성되어 다대다 관계가 형성된다.
- 한계
    - 실무에서 사용하지 않음
    - 연결 테이블이 단순히 연결만하지 않고 추가 데이터를 담음 (예시 참고: order_count, order_date)
```text
<Table>
member
    member_id (PK)
    username

product
    product_id (PK)
    name

member_product
    member_id (FK)
    product_id (FK)
    order_count
    order_date
```
- 한계 극복
    - 연결 테이블용 엔티티 추가 (ex03-model의 OrderItem 참고)
    - @ManyToMany -> @OneToMany, @ManyToOne 사용

## Annotation 상세
- @JoinColumn: 외래 키 매핑할 때 사용
    - name: 매핑할 외래 키 이름
    - referencedColumnName: 외래 키가 참조하는 대상 테이블의 컬럼명
    - foreignKey(DDL): 외래 키 제약 조건을 직접 지정할 수 있다. (테이블 생성 시에만 사용)
    - unique, nullable, updatable, columnDefinition, table 속성은 @Column과 같다.
- @ManyToOne
    - optional: false로 설정 시 연관된 엔티티가 항상 있어야 한다.
    - fetch: 글로벌 패치 전략 설정
        - @ManyToOne=FetchType.EAGER
        - @OneToMany=FetchType.LAZY
    - cascade: 영속성 전이 기능 사용
    - targetEntity: 연관된 엔티티의 타입 정보를 설정 (거의 사용 안함)
- @OneToMany
    - mappedBy: 연관관계 주인 필드명을 지정
    - fetch: 글로벌 패치 전략 설정
        - @ManyToOne=FetchType.EAGER
        - @OneToMany=FetchType.LAZY
    - cascade: 영속성 전이 기능을 사용
    - targetEntity: 연관된 엔티티의 타입 정보를 설정 (거의 사용 안함)