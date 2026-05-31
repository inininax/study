# ex08 프록시와 연관관계 관리 (Proxy, Fetch)
## 프록시
### 프록시 기초
- em.find() vs em.getReference()
- em.find(): 데이터베이스를 통해 실제 엔티티 객체 조회
- em.getReference(): 데이터베이스 조회를 미루는 가짜(프록시) 엔티티 객체 조회

### 프록시 특징
- 실제 클래스를 상속 받아서 만들어짐
- 실제 클래스와 겉 모양이 같다.
- 사용하는 입장에서는 진짜 객체인지 프록시 객체인지 구분하지 않고 사용하면 됨 (이론상)
- 프록시 객체는 실제 객체의 참조(target)를 보관
- 프록시 객체를 호출하면 프록시 객체는 실제 객체의 메소드 호출(delegate)

### 프록시 객체의 초기화
```text
Member member = new Member();
member.setUsername("hello");

em.persist(member);
em.flush();
em.clear();
```
```text
Member findMember = em.getReference(Member.class, member.getId());
System.out.println( findMember.getId() );       // 이미 존재하기 때문에 select 하지 않음
System.out.println( findMember.getUsername() ); // select query 실행
System.out.println( findMember.getClass() );    // proxy 객체 반환 - Member$HibernateProxy$hCqMCcnd
```

- 프록시 객체는 처음 사용할 때 한번만 초기화
  
- 프록시 객체를 초기화 할 때,
  프록시 객체가 실제 엔티티로 바뀌는 것은 아님,
  초기화되면 프록시 객체를 통해서 실제 엔티티에 접근 가능
  
- 프록시 객체는 원본 엔티티를 상속 받음, 따라서 타입 체크 시 주의해야함
  (== 비교 실패, 대신 instance of 사용)
  
- 영속성 컨텍스트에 찾는 엔티티가 이미 있을 경우에는 em.getReference()를 호출해도 실제 엔티티 반환
```text
// find() 호출 후 getReference() 호출 시
Member m1 = em.find(Member.class, member.getId());          // select query & Member.class 반환
System.out.println(m1.getClass());                          // Member.class

Member m2 = em.getReference(Member.class, member.getId());  // none query & Member.class 반환
                                                            // 이미 엔티티가 호출된 경우에는
                                                            // getReference를 사용해도 Proxy 객체가 아닌 실제 객체를 반환한다.
System.out.println(m2.getClass());                          // Member.class

System.out.println(m1 == m2); // true
```
```text
// getReference() 호출 후 find() 호출 시
Member m1 = em.getReference(Member.class, member.getId());  // Proxy 객체 반환
Member m2 = em.find(Member.class, member.getId());          // Member 객체를 반환할 것 같지만 Proxy 객체를 반환한다.
System.out.println(m1 == m2); // true
```

- 영속성 컨텍스트의 도움을 받을 수 없는 준 영속성 상태일 때, 프록시를 초기화하면 문제 발생
  (하이버네이트는 org.hibernate.LazyInitializationException 예외를 터트림)
```text
try {
    Member refMember = em.getReference(Member.class, member.getId());   // Proxy 객체 반환
    System.out.println(refMember);
    
    em.detach(refMember); // 영속성 해제
    // 또는 em.close();
    // 또는 em.clear();

    refMember.getUsername(); // ** exception 발생

} catch (Exception e) {
    e.printStackTrace(); // org.hibernate.LazyInitializationException - could not initialize proxy - no Session
}
```
  
### 프록시 확인
- 프록시 인스턴스의 초기화 여부 확인 (PersistenceUnitUtil.isLoaded)
```text
boolean isLoaded = emf.getPersistenceUnitUtil().isLoaded(refMember);
System.out.println("isLoaded=" + isLoaded);
```
  
- 프록시 클래스 확인 방법 (xx.getClass().getName() 출력 시 ..javasist.. or HibernateProxy...)

- 프록시 강제 초기화
```text
Member refMember = em.getReference(Member.class, member.getId());
System.out.println(refMember.getClass()); // Proxy 객체
refMember.getUsername(); // 이 때 초기화 실행됨 - select query 호출
```
```text
Member refMember = em.getReference(Member.class, member.getId());
System.out.println(refMember.getClass()); // Proxy 객체
org.hibernate.Hibernate.initialize(refMember); // 또는 강제로 초기화 실행할 경우
```
  
- 참고: JPA 표준은 강제 초기화 없음<br>
  (강제 호출: member.getName())



## 즉시 로딩과 지연 로딩
### 지연로딩 FetchType.LAZY
- 지연 로딩 FetchType.LAZY을 사용해서 프록시로 조회
- member 호출 후 team을 실제 사용하는 부분에서 조회함
```java
@Entity
public class Member {
    @ManyToOne(fetch = FetchType.LAZY) // **
    @JoinColumn(name = "TEAM_ID")
    private Team team;
}
```

### 즉시로딩 FetchType.EAGER
- 즉시 로딩 FetchType.EAGER 사용해서 프록시로 조회
- member 호출 시 team도 동시에 조회함
```java
@Entity
public class Member {
    @ManyToOne(fetch = FetchType.EAGER) // **
    @JoinColumn(name = "TEAM_ID")
    private Team team;
}
```

### 즉시로딩 주의점
- 가급적 지연로딩만 사용
- 즉시로딩을 적용하면 예상하지 못한 SQL이 발생 (?!)
- 즉시 로딩은 JPQL에서 N + 1 문제를 일으킨다. (** 모든 것을 지연로딩 처리하고 JPQL에서 FETCH JOIN을 사용해 처리)
- @ManyToOne, @OneToOne은 기본이 즉시 로딩 -> LAZY로 설정
- @OneToMany, @ManyToMany는 기본이 지연 로딩



## 지연 로딩 활용
- 가능한 모든 부분에 지연로딩 사용
- JPQL fetch 조인이나, 엔티티 그래프 기능을 사용해라.
- 즉시 로딩 시 상상하지 못한 쿼리가 실행 될 수 있다.



## 영속성 전이: CASCADE
### 영속성 전이: CASCADE 특징
- 특정 엔티티를 영속 상태로 만들 때 연관된 엔티티도 함께 영속 상태로 만들고 싶을 때
- 예: 부모 엔티티를 저장할 때 지식 엔티티도 함께 저장
- 영속성 전이는 연관관계를 매핑하는 것과 아무 관련이 없음
- 엔티티를 영속화할 때 연관된 엔티티도 함께 영속화하는 편리함 을 제공할 뿐

### cascade의 종류
- ALL: 모두 적용
- PERSIST: 영속
- REMOVE: 삭제
- MERGE: 병합
- REFERENCE: REFRESH
- DETACH: DETACH
```java
@OneToMany(mappedBy = "parent", cascade = CascadeType.ALL)      private List<Child> childList = new ArrayList<>(); 
@OneToMany(mappedBy = "parent", cascade = CascadeType.PERSIST)  private List<Child> childList = new ArrayList<>();
@OneToMany(mappedBy = "parent", cascade = CascadeType.MERGE)    private List<Child> childList = new ArrayList<>();
@OneToMany(mappedBy = "parent", cascade = CascadeType.REMOVE)   private List<Child> childList = new ArrayList<>();
@OneToMany(mappedBy = "parent", cascade = CascadeType.REFRESH)  private List<Child> childList = new ArrayList<>();
@OneToMany(mappedBy = "parent", cascade = CascadeType.DETACH)   private List<Child> childList = new ArrayList<>();
```


## 고아 객체
### 고아 객체
- 고아 객체 제거: 부모 엔티티와 연관관계가 끊어진 자식 엔티티 를 자동으로 삭제
- @OneToMany(mappedBy = "parent", orphanRemoval = true)
```java
Parent parent1 = em.find(Parent.class, id);
parent1.getChildren().remove(0);
//자식 엔티티를 컬렉션에서 제거 시 DELETE FROM CHILD WHERE ID=? 가 자동으로 실행된다. 
```

### 고아객체 주의점
- 참조가 제거된 엔티티는 다른 곳에서 참조하지 않는 고아객체로 보고 삭제하는 기능
- 참조하는 곳이 하나일 때 사용해야함!
- 특정 엔티티가 개인 소유할 때 사용
- @OneToOne, @OneToMany만 가능
- 참고: 개념적으로 부모를 제거하면 자식은 고아가 된다. 따라서 고아 객체 제거 기능을 활성화 하면, 부모를 제거할 때 자식도 함께 제거된다.
  이것이 CascadeType.REMOVE처럼 동작한다.



## 영속성 전이 + 고아 객체, 생명주기
- CascadeType.ALL + orphanRemovel=true
- 스스로 생명주기를 관리하는 엔티티는 em.persist()로 영속화, em.remove()로 제거
- 두 옵션을 모두 활성화 하면 부모 엔티티를 통해서 자식의 생명 주기를 관리할 수 있음
- 도메인 주도 설계(DDD)의 Aggregate Root개념을 구현할 때 유용


## 글로벌 패치 전략 설정
- 모든 연관관계를 지연 로딩으로 설정
- @ManyToOne, @OneToOne은 기본이 즉시 로딩이므로 지연 로딩으로 변경

## 영속성 전이 설정
- Order -> Delivery를 영속성 전이 ALL 설정
- Order -> OrderItem을 영속성 전이 ALL 설정