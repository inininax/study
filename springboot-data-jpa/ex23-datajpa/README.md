# ex23 - DATA JPA Example

## 참고
- [JPA Repositories - Query Creation](https://docs.spring.io/spring-data/jpa/docs/current/reference/html/#jpa.query-methods.query-creation)
- [Spring DATA Repositories - Query Creation](https://docs.spring.io/spring-data/jpa/docs/current/reference/html/#repositories.query-methods.query-creation)
- [Limiting Query Results](https://docs.spring.io/spring-data/jpa/docs/current/reference/html/#repositories.limit-query-result)

## 프로젝트 환경 설정
- [build.gradle](./build.gradle)
- [application.yml](./src/main/resources/application.yml)
- [테스트 컨트롤러](./src/test/java/study/datajpa/BaseTest.java)

## 인터페이스 설정
### 공통 인터페이스 설정
- JavaConfig 설정 - 스프링 부트 사용시 생략 가능
- 스프링 부트 사용 시 @SpringBootApplication 위치를 지정 (해당 패키지와 하위 패키지 인식)
- 만약 위치가 달라지면 @EnableJpaRepositories 필요
```java
@Configuration
@EnableJpaRepositories(basePackages = "study.datajpa.repository")
public class AppConfig {}
```

### 공통 인터페이스 적용
- 순수 JPA로 구현한 MemberJpaRepository 대신에 스프링 데이터 JPA가 제공하는 공통 인터페이스 사용
```java
public interface MemberRepository extends JpaRepository<Member, Long> {
}
```

## 기능
### JPA NamedQuery
```java
@Entity
@NamedQuery(
        name = "Member.findByUsername",
        query = "select m from Member m where m.username = :username"
)
public class Member extends BaseEntity {
}
```
```java
public interface MemberRepository extends JpaRepository<Member, Long>, MemberRepositoryCustom {
    //@Query 를 생략하고 메서드 이름만으로 Named 쿼리를 호출할 수 있다.
    @Query(name = "Member.findByUsername")
    List<Member> findByUsername(@Param("username") String username);
}
```

### @Query, 값, DTO 조회하기
- DTO로 직접 조회
```java
public interface MemberRepository extends JpaRepository<Member, Long>, MemberRepositoryCustom {
    @Query("select new study.datajpa.dto.MemberDto(m.id, m.username, t.name) " +
            "from Member m join m.team t")
    List<MemberDto> findMemberDto();
}
```

### 파라미터 바인딩
- 파라미터 바인딩
- 컬렉션 파라미터 바인딩
```java
import org.springframework.data.repository.query.Param;

public interface MemberRepository extends JpaRepository<Member, Long> {
    @Query("select m from Member m where m.username = :name")
    Member findMembers(@Param("name") String username);
    
    @Query("select m from Member m where m.username in :names")
    List<Member> findByNames(@Param("names") List<String> names);
}
```

### 반환 타입
- [스프링 데이터 JPA 공식 문서](https://docs.spring.io/spring-data/jpa/docs/current/reference/html/#repository-query-return-types)
```text
List<Member> findByUsername(String name);     //컬렉션
Member findByUsername(String name);           //단건
Optional<Member> findByUsername(String name); //단건 Optional
```

- 조회 결과가 많거나 없으면?
  - 컬렉션
    - 결과 없음: 빈 컬렉션 반환
  - 단건 조회
    - 결과 없음: null 반환
    - 결과가 2건 이상: javax.persistence.NonUniqueResultException 예외 발생
- 참고
  - 단건으로 지정한 메서드를 호출하면 스프링 데이터 JPA는 내부에서 JPQL의 Query.getSingleResult() 메서드를 호출한다.
  - 이 메서드를 호출했을 때 조회 결과가 없으면 javax.persistence.NoResultException 예외가 발생하는데 개발자 입장에서 다루기가 상당히 불편하다.
  - 스프링 데이터 JPA는 단건을 조회할 때 이 예외가 발생하면 예외를 무시하고 대신에 null을 반환한다.

### 스프링 데이터 JPA 페이징과 정렬
- 페이징과 정렬 파라미터
  - org.springframework.data.domain.Sort : 정렬 기능
  - org.springframework.data.domain.Pageable : 페이징 기능 (내부에 Sort 포함)
- 특별한 반환 타입
  - org.springframework.data.domain.Page : 추가 count 쿼리 결과를 포함하는 페이징
  - org.springframework.data.domain.Slice : 추가 count 쿼리 없이 다음 페이지만 확인 가능 (내부적으로 limit + 1조회)
  - List (자바 컬렉션): 추가 count 쿼리 없이 결과만 반환
- 페이징과 정렬 사용 예제
```text
Page<Member> findByUsername(String name, Pageable pageable); //count 쿼리 사용 Slice<Member> findByUsername(String name, Pageable pageable); //count 쿼리 사용 안함
List<Member> findByUsername(String name, Pageable pageable); //count 쿼리 사용 안함
List<Member> findByUsername(String name, Sort sort);
```
- Page 인터페이스
```java
public interface Page<T> extends Slice<T> {
	static <T> Page<T> empty() {
		return empty(Pageable.unpaged());
	}
	
	static <T> Page<T> empty(Pageable pageable) {
		return new PageImpl<>(Collections.emptyList(), pageable, 0);
	}
	
	int getTotalPages();
	long getTotalElements();
	<U> Page<U> map(Function<? super T, ? extends U> converter);
}
```
- Slice 인터페이스
```java
public interface Slice<T> extends Streamable<T> {
	int getNumber();
	int getSize();
	int getNumberOfElements();
	List<T> getContent();
	boolean hasContent();
	Sort getSort();
	boolean isFirst();
	boolean isLast();
	boolean hasNext();
	boolean hasPrevious();

	default Pageable getPageable() {
		return PageRequest.of(getNumber(), getSize(), getSort());
	}

	Pageable nextPageable();
	Pageable previousPageable();
	<U> Slice<U> map(Function<? super T, ? extends U> converter);

	default Pageable nextOrLastPageable() {
		return hasNext() ? nextPageable() : getPageable();
	}

	default Pageable previousOrFirstPageable() {
		return hasPrevious() ? previousPageable() : getPageable();
	}
}
```
- count 쿼리를 다음과 같이 분리할 수 있음
```text
@Query(value = “select m from Member m”, 
       countQuery = “select count(m.username) from Member m”)
Page<Member> findMemberAllCountBy(Pageable pageable);
```
- [Top, First 사용 참고](https://docs.spring.io/spring-data/jpa/docs/current/reference/html/#repositories.limit-query-result)
```text
List<Member> findTop3By();
```
- 페이지를 유지하면서 엔티티를 DTO로 변환하기
```text
Page<Member> page = memberRepository.findByAge(10, pageRequest);
Page<MemberDto> dtoPage = page.map(m -> new MemberDto());
```

### 벌크성 수정, 삭제 쿼리
- 벌크성 수정, 삭제 쿼리는 @Modifying 어노테이션을 사용
  - 사용하지 않으면 다음 예외 발생
  - org.hibernate.hql.internal.QueryExecutionRequestException: Not supported for DML operations
- 벌크성 쿼리를 실행하고 나서 영속성 컨텍스트 초기화: @Modifying(clearAutomatically = true) (이 옵션의 기본값은 false)
  - 이 옵션 없이 회원을 findById로 다시 조회하면 영속성 컨텍스트에 과거 값이 남아서 문제가 될 수 있다. 만약 다시 조회해야 하면 꼭 영속성 컨텍스트를 초기화 하자.
- 참고: 벌크 연산은 영속성 컨텍스트를 무시하고 실행하기 때문에, 영속성 컨텍스트에 있는 엔티티의 상태와 DB에 엔티티 상태가 달라질 수 있다.
  - 권장하는 방안
    - 영속성 컨텍스트에 엔티티가 없는 상태에서 벌크 연산을 먼저 실행한다.
    - 부득이하게 영속성 컨텍스트에 엔티티가 있으면 벌크 연산 직후 영속성 컨텍스트를 초기화 한다.
```text
@Modifying
@Query("update Member m set m.age = m.age + 1 where m.age >= :age")
int bulkAgePlus(@Param("age") int age);
```

### @EntityGraph
- 연관된 엔티티들을 SQL 한번에 조회하는 방법
- member team은 지연로딩 관계이다. 따라서 다음과 같이 team의 데이터를 조회할 때 마다 쿼리가 실행된다. (N+1 문제 발생)

#### JPQL 페치 조인
```text
@Query("select m from Member m left join fetch m.team")
List<Member> findMemberFetchJoin();
```

#### EntityGraph
- 사실상 페치 조인(FETCH JOIN)의 간편 버전
- LEFT OUTER JOIN 사용
```text
//공통 메서드 오버라이드
@Override
@EntityGraph(attributePaths = {"team"})
List<Member> findAll();

//JPQL + 엔티티 그래프
@EntityGraph(attributePaths = {"team"})
@Query("select m from Member m") List<Member> findMemberEntityGraph();

//메서드 이름으로 쿼리에서 특히 편리하다.
@EntityGraph(attributePaths = {"team"})
List<Member> findByUsername(String username)
```

#### NamedEntityGraph 사용 방법
```text
@NamedEntityGraph(name = "Member.all", attributeNodes =
@NamedAttributeNode("team"))
@Entity
public class Member {}
```
```text
@EntityGraph("Member.all")
@Query("select m from Member m")
List<Member> findMemberEntityGraph();
```

### JPA Hint & Lock
#### read only
- Update Query 실행X
```text
@QueryHints(value = @QueryHint(name = "org.hibernate.readOnly", value = "true"))
Member findReadOnlyByUsername(String username);
```

- org.springframework.data.jpa.repository.QueryHints 어노테이션을 사용
- forCounting : 반환 타입으로 Page 인터페이스를 적용하면 추가로 호출하는 페이징을 위한 count 쿼리도 쿼리 힌트 적용 (기본값 true)
```text
@QueryHints(
    value = { @QueryHint(name = "org.hibernate.readOnly", value = "true") },
    forCounting = true
)
Page<Member> findByUsername(String name, Pagable pageable);
```

#### Lock
```text
@Lock(LockModeType.PESSIMISTIC_WRITE)
List<Member> findByUsername(String name);
```
- org.springframework.data.jpa.repository.Lock 어노테이션을 사용
- JPA가 제공하는 락은 JPA 책 16.1 트랜잭션과 락 절을 참고

## 확장 기능
### 사용자 정의 리포지토리 구현
- 스프링 데이터 JPA 리포지토리는 인터페이스만 정의하고 구현체는 스프링이 자동 생성
- 스프링 데이터 JPA가 제공하는 인터페이스를 직접 구현하면 구현해야 하는 기능이 너무 많음
- 다양한 이유로 인터페이스의 메서드를 직접 구현하고 싶다면?
  - JPA 직접 사용( EntityManager )
  - 스프링 JDBC Template 사용
  - MyBatis 사용
  - 데이터베이스 커넥션 직접 사용 등등...
  - Querydsl 사용

- 사용자 정의 인터페이스
```java
public interface MemberRepositoryCustom {
    List<Member> findMembersCustom();
}
```
- 사용자 정의 인터페이스 구현 클래스
```java
@RequiredArgsConstructor
public class MemberRepositoryCustomImpl implements MemberRepositoryCustom {
    private final EntityManager em;

    @Override
    public List<Member> findMembersCustom() {
        return em.createQuery("select m from Member m", Member.class)
                .getResultList();
    }
}
```
- 사용자 정의 인터페이스 상속
```java
public interface MemberRepository extends JpaRepository<Member, Long>, MemberRepositoryCustom {
}
```
- 사용자 정의 메서드 호출 코드
```text
List<Member> result = memberRepository.findMemberCustom();
```

- 사용자 정의 구현 클래스
  - 규칙: 리포지토리 인터페이스 이름 + Impl
  - 스프링 데이터 JPA가 인식해서 스프링 빈으로 등록
  - Impl 대신 다른 이름으로 변경하고 싶으면?
```java
@EnableJpaRepositories(basePackages = "study.datajpa.repository", repositoryImplementationPostfix = "Impl")
@Configuration
public class AppConfig {
}
```

### Auditing
- 엔티티를 생성, 변경할 때 변경한 사람과 시간을 추적하고 싶으면?
  - 등록일 수정일 등록자 수정자
- JPA 주요 이벤트 어노테이션
  - @PrePersist, @PostPersist
  - @PreUpdate, @PostUpdate
- 설정
  - @EnableJpaAuditing 스프링 부트 설정 클래스에 적용해야함
```java
@EnableJpaRepositories(basePackages = "study.datajpa.repository", repositoryImplementationPostfix = "Impl")
@EnableJpaAuditing
@Configuration
public class AppConfig {
}
```
- 어노테이션
  - @CreatedDate
  - @LastModifiedDate
  - @CreatedBy
  - @LastModifiedBy
```java
@EntityListeners(AuditingEntityListener.class)
@MappedSuperclass
@Getter
public class BaseTimeEntity {
    @CreatedDate
    @Column(updatable = false)
    private LocalDateTime createdDate;

    @LastModifiedDate
    private LocalDateTime lastModifiedDate;
}

@EntityListeners(AuditingEntityListener.class)
@MappedSuperclass
@Getter
public class BaseEntity extends BaseTimeEntity {
    @CreatedBy
    @Column(updatable = false)
    private String createdBy;

    @LastModifiedBy
    private String lastModifiedBy;
}
```

- 등록자, 수정자를 처리해주는 AuditorAware 스프링 빈 등록
```java
@EnableJpaRepositories(basePackages = "study.datajpa.repository", repositoryImplementationPostfix = "Impl")
@EnableJpaAuditing
@Configuration
public class AppConfig {
    //실무에서는 spring security login 정보를 id로 활용
    @Bean
    public AuditorAware<String> auditorAware() {
        //spring security holder에서 정보를 가져와 출력
        return () -> Optional.of(UUID.randomUUID().toString());
    }
}
```

### Web 확장 - 도메인 클래스 컨버터, 페이징과 정렬
- page 0부터 시작하는 제약 사항 발생
```java
@RestController
@RequiredArgsConstructor
public class MemberController {

    private final MemberRepository memberRepository;

    @PostConstruct
    public void init() {
        for (int i = 0; i < 110; i++) {
            memberRepository.save(new Member("user" + i, i));
        }
    }

    @GetMapping("/mebers/{id}")
    public String findMember(@PathVariable("id") Long id) {
        Member member = memberRepository.findById(id).get();
        return member.getUsername();
    }

    //domain class converter - 조회용으로만 사용
    //주의: 도메인 클래스 컨버터로 엔티티를 파라미터로 받으면, 이 엔티티는 단순 조회용으로만 사용해야 한다.
    //(트랜잭션이 없는 범위에서 엔티티를 조회했으므로, 엔티티를 변경해도 DB에 반영되지 않는다.)
    @GetMapping("/mebers2/{id}")
    public String findMember(@PathVariable("id") Member member) {
        return member.getUsername();
    }

    @GetMapping("/members")
    public Page<MemberDto> list(@PageableDefault(size = 5, sort = "username") Pageable pageable) {
        return memberRepository.findAll(pageable)
                .map(MemberDto::new);
    }
}
```

## 새로운 엔티티를 구별하는 방법
- save() 메서드
  - 새로운 엔티티면 저장( persist )
  - 새로운 엔티티가 아니면 병합( merge )
- 새로운 엔티티를 판단하는 기본 전략
  - 식별자가 객체일 때 null 로 판단
  - 식별자가 자바 기본 타입일 때 0 으로 판단
  - Persistable 인터페이스를 구현해서 판단 로직 변경 가능

### Persistable 구현
- @GeneratedValue를 사용하지 않고 강제로 ID를 세팅하는 경우
- implements Persistable<ID>를 사용하여 getId(), isNew()를 구현함으로써
- JPA 내부 로직에서 em.merge가 호출되는 것을 막을 수 있다.<br>(merge는 select를 호출하며 merge 보다는 변경 감지를 사용할 것을 권장)
```java
package org.springframework.data.domain;
public interface Persistable<ID> {
    ID getId();
    boolean isNew();
}
```
```java
@Entity
@EntityListeners(AuditingEntityListener.class)
@NoArgsConstructor(access = AccessLevel.PROTECTED)
public class Item implements Persistable<String> {
    @Id
    private String id;

    @CreatedDate
    private LocalDateTime createdDate;

    public Item(String id) {
        this.id = id;
    }

    @Override
    public String getId() {
        return id;
    }

    @Override
    public boolean isNew() {
        return createdDate == null;
    }
}
```

### 나머지 기능들
#### Specifications: 사용안함 (MemberSpec, MemberRepositoryTest 참고)
#### Query By Example: 사용안함 (MemberRepositoryTest 참고)
#### Projections: 사용안함
#### 네이티브 쿼리
- JPQL은 위치 기반 파리미터를 1부터 시작하지만 네이티브 SQL은 0부터 시작
```java
public interface MemberRepository extends JpaRepository<Member, Long> {
    @Query(value = "select * from member where username = ?", nativeQuery = true)
    Member findByNativeQuery(String username);
    
    @Query(value = "SELECT m.member_id as id, m.username, t.name as teamName " +
                  "FROM member m left join team t",
                  countQuery = "SELECT count(*) from member",
                  nativeQuery = true)
    Page<MemberProjection> findByNativeProjection(Pageable pageable);
}

public interface MemberProjection {
    Long getId();
    String getUsername();
    String getTeamName();
}
```