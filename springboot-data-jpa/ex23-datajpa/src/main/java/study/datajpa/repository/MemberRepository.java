package study.datajpa.repository;

import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.*;
import org.springframework.data.repository.query.Param;
import study.datajpa.dto.MemberDto;
import study.datajpa.entity.Member;

import javax.persistence.LockModeType;
import javax.persistence.QueryHint;
import java.util.List;

public interface MemberRepository extends JpaRepository<Member, Long>, MemberRepositoryCustom, JpaSpecificationExecutor<Member> {

    List<Member> findByUsernameAndAgeGreaterThan(String username, int age);

    //Named Query - @Query 생략 가능 (Named 쿼리, 실무에서는 잘 사용하지 않음) - Named Query 사용 시 @Param 필요함
    @Query(name = "Member.findByUsername")
    List<Member> findByUsername(@Param("username") String username);

    //메서드에 JPQL 쿼리 작성
    @Query("select m from Member m where m.username = :username and m.age = :age")
    List<Member> findMember(@Param("username") String username, @Param("age") int age);

    /*
        반환 타입 예시
        List<Member> findByUsername(String name);
        Member findByUsername(String name);
        Optional<Member> findByUsername(String name);

        참고: https://docs.spring.io/spring-data/jpa/docs/current/reference/ html/#repository-query-return-types
    */

    //@Embedded도 조회 가능하다.
    @Query("select m.username from Member m")
    List<String> findUsernameList();

    //dto
    @Query("select new study.datajpa.dto.MemberDto(m.id, m.username, t.name) " +
            "from Member m join m.team t")
    List<MemberDto> findMemberDto();

    @Query("select m from Member m where m.username = :name")
    Member findMembers(@Param("name") String username);

    @Query("select m from Member m where m.username in :names")
    List<Member> findByNames(@Param("names") List<String> names);

    //실행되는 쿼리
    //select m        from Member m where m.age = ? order by m.username desc limit ?
    //select count(m) from Member m where m.age = ?
    Page<Member> findByAge(int age, Pageable pageable); //count 쿼리 사용

    //다른 방법 (Slice: count 쿼리 실행 안함, limit + 1 조회, 모바일 더보기와 같이)
    //Slice<Member> findByAge(int age, Pageable pageable); //count 쿼리 사용 (3개를 조회 요청하면 3+1개를 조회하여 다음 페이지가 있는지 확인)
    //List<Member> findByAge(int age, Pageable pageable); //count 쿼리 사용

    //count 직접 구현
    @Query(value = "select m from Member m left join m.team as t",
            countQuery = "select count(m.username) from Member m")
    Page<Member> findMemberAllCountBy(Pageable pageable);

    //벌크성 수정, 삭제 쿼리는 @Modifying 어노테이션을 사용
    //벌크성 쿼리를 실행하고 나서 영속성 컨텍스트 초기화, 이와 같은 방법도 존재함 @Modifying(clearAutomatically = true)
    @Modifying(flushAutomatically = true, clearAutomatically = true)
    @Query("update Member m set m.age = m.age + 1 where m.age >= :age")
    int bulkAgePlus(@Param("age") int age);

    @Query("select m from Member m left join fetch m.team t")
    List<Member> findMembersFetchJoin();

    @Override
    @EntityGraph(attributePaths = {"team"})
    List<Member> findAll();

    @EntityGraph(attributePaths = {"team"})
    @Query("select m from Member m")
    List<Member> findMembersEntityGraph();

    //@EntityGraph("Member.all") 또는 @EntityGraph(attributePaths = {"team"})
    //Entity에 미리 정의한 것을 불러와서 사용
    @EntityGraph("Member.all")
    List<Member> findEntityGraph1ByUsername(@Param("username") String username);

    //@EntityGraph("Member.all") 또는 @EntityGraph(attributePaths = {"team"})
    @EntityGraph(attributePaths = {"team"})
    List<Member> findEntityGraph2ByUsername(@Param("username") String username);

    //최적화 시 readOnly 이기 때문에 hibernate 내부 비교 로직을 생성하지 않아 미미하게나마 메모리를 사용하지 않음
    //사용 요도가 매우 많거나 아주 극심한 최적화가 필요할 경우 사용
    @QueryHints(value = {@QueryHint(name = "org.hibernate.readOnly", value = "true")})
    Member findReadOnlyByUsername(String username);

    @QueryHints(value = {@QueryHint(name = "org.hibernate.readOnly", value = "true")}, forCounting = true)
    Page<Member> findReadOnlyPageByUsername(String username, Pageable pageable);

    @Lock(LockModeType.PESSIMISTIC_WRITE)
    List<Member> findLockByUsername(String username);

    @Query(value = "select * from member where username = ?", nativeQuery = true)
    Member findByNativeQuery(String username);

    @Query(value = "SELECT m.member_id as id, m.username, t.name as teamName" +
            " FROM member m" +
            " left join team t on (m.team_id = t.team_id)" +
            " order by m.member_id desc, t.team_id desc",
            countQuery = "SELECT count(*) from member",
            nativeQuery = true)
    Page<MemberProjection> findByNativeProjection(Pageable pageable);
}