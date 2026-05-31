package study.datajpa.repository;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.domain.*;
import org.springframework.data.jpa.domain.Specification;
import study.datajpa.BaseTest;
import study.datajpa.dto.MemberDto;
import study.datajpa.entity.Member;
import study.datajpa.entity.Team;

import javax.persistence.EntityManager;
import javax.persistence.PersistenceContext;
import java.util.List;

import static org.assertj.core.api.Assertions.assertThat;

public class MemberRepositoryTest extends BaseTest {

    private static final Logger log = LoggerFactory.getLogger(MemberRepositoryTest.class);

    @PersistenceContext
    EntityManager em;

    @Autowired
    MemberRepository memberRepository;

    @Autowired
    TeamRepository teamRepository;

    @Test
    void testMember() {
        Member member = new Member("memberA");
        Member savedMember = memberRepository.save(member);
        Member findMember = memberRepository.findById(savedMember.getId()).get();

        assertThat(findMember.getId()).isEqualTo(member.getId());
        assertThat(findMember.getUsername()).isEqualTo(member.getUsername());
        assertThat(findMember).isEqualTo(member); //JPA 엔티티 동일
    }

    @Test
    void basicCRUD() {
        Member member1 = new Member("member1");
        Member member2 = new Member("member2");
        memberRepository.save(member1);
        memberRepository.save(member2);

        //단건 조회 검증
        Member findMember1 = memberRepository.findById(member1.getId()).get();
        Member findMember2 = memberRepository.findById(member2.getId()).get();
        assertThat(findMember1).isEqualTo(member1);
        assertThat(findMember2).isEqualTo(member2);

        //리스트 검증
        List<Member> all = memberRepository.findAll();
        assertThat(all.size()).isEqualTo(2);

        //카운트 검증
        long count = memberRepository.count();
        assertThat(count).isEqualTo(2);

        //삭제 검증
        memberRepository.delete(member1);
        memberRepository.delete(member2);
        long deletedCount = memberRepository.count();
        assertThat(deletedCount).isEqualTo(0);
    }

    @Test
    void findByUsernameAndAgeGreaterThan() {
        Member m1 = new Member("AAA", 10);
        Member m2 = new Member("AAA", 20);
        memberRepository.save(m1);
        memberRepository.save(m2);

        List<Member> result = memberRepository.findByUsernameAndAgeGreaterThan("AAA", 15);

        assertThat(result.get(0).getUsername()).isEqualTo("AAA");
        assertThat(result.get(0).getAge()).isEqualTo(20);
        assertThat(result.size()).isEqualTo(1);
    }

    @Test
    void paging() {
        //given
        Team teamA = teamRepository.save(new Team("TeamA"));
        Team teamB = teamRepository.save(new Team("TeamB"));
        memberRepository.save(new Member("member1", 10, teamA));
        memberRepository.save(new Member("member2", 10, teamA));
        memberRepository.save(new Member("member3", 10, teamB));
        memberRepository.save(new Member("member4", 10, teamB));
        memberRepository.save(new Member("member5", 10, teamB));

        int age = 10;
        int offset = 0;
        int limit = 3;

        //when
        PageRequest pageRequest = PageRequest.of(offset, limit, Sort.by(Sort.Direction.DESC, "username"));
        Page<Member> page = memberRepository.findByAge(age, pageRequest);
        Page<MemberDto> toMap = page.map(m -> new MemberDto(m.getId(), m.getUsername(), m.getTeam() == null ? null : m.getTeam().getName()));
        log.debug("dtoPage: {}", toMap); // dtoPage: Page 1 of 2 containing study.datajpa.dto.MemberDto instances

        //then
        List<Member> content = page.getContent(); //조회된 데이터
        assertThat(content.size()).isEqualTo(3); //조회된 데이터 수
        assertThat(page.getTotalElements()).isEqualTo(5); //전체 데이터 수
        assertThat(page.getNumber()).isEqualTo(0); //페이지 번호
        assertThat(page.getTotalPages()).isEqualTo(2); //전체 페이지 수
        assertThat(page.isFirst()).isTrue(); //첫번째페이지
        assertThat(page.isLast()).isFalse(); //마지막페이지
        assertThat(page.hasNext()).isTrue(); //다음페이지가 있는가?o
    }

    @Test
    void paging_countQuery() {
        //given
        Team teamA = teamRepository.save(new Team("TeamA"));
        Team teamB = teamRepository.save(new Team("TeamB"));
        memberRepository.save(new Member("member1", 10, teamA));
        memberRepository.save(new Member("member2", 10, teamA));
        memberRepository.save(new Member("member3", 10, teamB));
        memberRepository.save(new Member("member4", 10, teamB));
        memberRepository.save(new Member("member5", 10, teamB));

        int offset = 0;
        int limit = 3;

        //when
        PageRequest pageRequest = PageRequest.of(offset, limit, Sort.by(Sort.Direction.DESC, "username"));
        Page<Member> page = memberRepository.findMemberAllCountBy(pageRequest);
        Page<MemberDto> toMap = page.map(m -> new MemberDto(m.getId(), m.getUsername(), m.getTeam() == null ? null : m.getTeam().getName()));
        log.debug("dtoPage: {}", toMap); // dtoPage: Page 1 of 2 containing study.datajpa.dto.MemberDto instances

        //then
        List<Member> content = page.getContent(); //조회된 데이터
        assertThat(content.size()).isEqualTo(3); //조회된 데이터 수
        assertThat(page.getTotalElements()).isEqualTo(5); //전체 데이터 수
        assertThat(page.getNumber()).isEqualTo(0); //페이지 번호
        assertThat(page.getTotalPages()).isEqualTo(2); //전체 페이지 수
        assertThat(page.isFirst()).isTrue(); //첫번째페이지
        assertThat(page.isLast()).isFalse(); //마지막페이지
        assertThat(page.hasNext()).isTrue(); //다음페이지가 있는가?o
    }

    @Test
    @DisplayName("JPA를 사용한 벌크성 수정 쿼리 테스트")
    void bulkUpdate() {
        //given
        Team teamA = teamRepository.save(new Team("TeamA"));
        Team teamB = teamRepository.save(new Team("TeamB"));
        memberRepository.save(new Member("member1", 10, teamA));
        memberRepository.save(new Member("member2", 10, teamA));
        memberRepository.save(new Member("member3", 20, teamB));
        memberRepository.save(new Member("member4", 21, teamB));
        memberRepository.save(new Member("member5", 40, teamB));

        //when
        int resultCount = memberRepository.bulkAgePlus(20);

        //then
        assertThat(resultCount).isEqualTo(3);
    }

    @Test
    void findMemberLazy() {
        //given
        //member1 -> teamA
        //member2 -> teamB
        Team teamA = new Team("teamA");
        Team teamB = new Team("teamB");
        teamRepository.save(teamA);
        teamRepository.save(teamB);

        Member member1 = new Member("member1", 10, teamA);
        Member member2 = new Member("member2", 20, teamB);
        memberRepository.save(member1);
        memberRepository.save(member2);

        em.flush();
        em.clear();

        //when
        //List<Member> members = memberRepository.findAll();              //JpaRepository.findAll origin
        //List<Member> members = memberRepository.findMembersFetchJoin(); //fetch join
        //List<Member> members = memberRepository.findAll();              //JpaRepository.findAll override
        List<Member> members = memberRepository.findMembersEntityGraph(); //EntityGraph 직접 사용 시

        //then
        for (Member member : members) {
            log.debug("member = {}", member.getUsername());

            //findAll                : class study.datajpa.entity.Team$HibernateProxy$ujeEh2nU
            //findMembersFetchJoin   : class study.datajpa.entity.Team
            //findAll override       : class study.datajpa.entity.Team (@EntityGraph(attributePaths = {"team"}) 사용 시)
            //findMembersEntityGraph : class study.datajpa.entity.Team (@EntityGraph(attributePaths = {"team"}) 사용 시)
            log.debug("member.teamClass = {}", member.getTeam().getClass());
            log.debug("member.team = {}", member.getTeam().getName());

            member.getTeam().getName();
        }

        /*
            *참고: 다음과 같이 지연 로딩 여부를 확인할 수 있다.

            //Hibernate 기능으로 확인
            Hibernate.isInitialized(member.getTeam())

            //JPA 표준 방법으로 확인
            PersistenceUnitUtil util = em.getEntityManagerFactory().getPersistenceUnitUtil(); util.isLoaded(member.getTeam());
        */
    }

    @Test
    void queryHint() {
        //given
        memberRepository.save(new Member("member1", 10));
        em.flush();
        em.clear();

        //when
        Member member = memberRepository.findReadOnlyByUsername("member1");
        member.setUsername("member2");

        em.flush(); //Update Query 실행 안함
    }

    @Test
    void pageQueryHint() {
        //given
        memberRepository.save(new Member("member1", 10));
        memberRepository.save(new Member("member2", 20));
        memberRepository.save(new Member("member3", 30));
        em.flush();
        em.clear();

        //when
        PageRequest pageRequest = PageRequest.of(0, 100, Sort.by(Sort.Direction.DESC, "username"));
        Page<Member> page = memberRepository.findReadOnlyPageByUsername("member1", pageRequest);
        page.forEach(member -> member.setUsername("member2"));

        em.flush(); //Update Query 실행 안함
    }

    @Test
    void lock() {
        //given
        Member member1 = new Member("member1", 10);
        memberRepository.save(member1);
        em.flush();
        em.clear();

        //when (select ... from ... for update)
        List<Member> findMembers = memberRepository.findLockByUsername("member1");
    }

    @Test
    void callCustom() {
        List<Member> result = memberRepository.findMembersCustom();
    }

    @Test
    void jpaEventBaseEntity() throws InterruptedException {
        //given
        Member member = new Member("member1");
        memberRepository.save(member);

        Thread.sleep(100);
        member.setUsername("member2");

        em.flush();
        em.clear();

        //when
        Member findMember = memberRepository.findById(member.getId()).get();

        //then
        log.debug("findMember.createdDate = {}", findMember.getCreatedDate());
        //log.debug("findMember.updatedDate = {}", findMember.getUpdatedDate());
        log.debug("findMember.lastModifiedDate = {}", findMember.getLastModifiedDate());
        log.debug("findMember.createdBy = {}", findMember.getCreatedBy());
        log.debug("findMember.lastModifiedBy = {}", findMember.getLastModifiedBy());
    }

    @Test
    void specBasic() {
        //given
        Team teamA = new Team("teamA1");
        em.persist(teamA);

        Member member1 = new Member("memberA1", 0, teamA);
        Member member2 = new Member("memberA2", 0, teamA);
        em.persist(member1);
        em.persist(member2);

        em.flush();
        em.clear();

        //when
        Specification<Member> spec = MemberSpec.username("memberA1").and(MemberSpec.teamName("teamA1"));
        List<Member> result = memberRepository.findAll(spec);

        //then
        assertThat(result.size()).isEqualTo(1);
    }

    @Test
    void queryByExample() {
        //given
        Team teamA = new Team("teamA1");
        em.persist(teamA);

        Member member1 = new Member("memberA1", 0, teamA);
        Member member2 = new Member("memberA2", 0, teamA);
        em.persist(member1);
        em.persist(member2);

        em.flush();
        em.clear();

        //when
        //Probe 생성
        Member member = new Member("memberA1");
        Team team = new Team("teamA"); //내부조인으로 teamA 가능
        member.setTeam(team);

        //ExampleMatcher 생성, age 프로퍼티는 무시
        ExampleMatcher matcher = ExampleMatcher.matching().withIgnorePaths("age");
        Example<Member> example = Example.of(member, matcher);
        List<Member> result = memberRepository.findAll(example);

        //then
        assertThat(result.size()).isEqualTo(1);
    }

    @Test
    void nativeQuery() {
        //given
        Team teamA = new Team("teamA1");
        em.persist(teamA);

        Member member1 = new Member("memberA1", 0, teamA);
        Member member2 = new Member("memberA2", 0, teamA);
        em.persist(member1);
        em.persist(member2);

        em.flush();
        em.clear();

        //when
        Pageable pageable = PageRequest.of(1, 10);
        Page<MemberProjection> result = memberRepository.findByNativeProjection(pageable);
        List<MemberProjection> content = result.getContent();

        for (MemberProjection memberProjection : content) {
            log.debug("memberProjection.userName = {}", memberProjection.getUsername());
            log.debug("memberProjection.teamName = {}", memberProjection.getTeamName());
        }

        //then
    }

}
