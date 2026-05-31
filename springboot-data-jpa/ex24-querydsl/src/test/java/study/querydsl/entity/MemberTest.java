package study.querydsl.entity;

import lombok.extern.slf4j.Slf4j;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.context.ActiveProfiles;
import org.springframework.transaction.annotation.Transactional;

import javax.persistence.EntityManager;
import java.util.List;

@Slf4j
@ActiveProfiles("testgroup")
@SpringBootTest
@Transactional
class MemberTest {
    @Autowired EntityManager em;

    @Test
    void testEntity() {
        saveTestData();

        em.flush();
        em.clear();

        List<Member> findMembers = em.createQuery("select m from Member m", Member.class)
                .getResultList();

        for (Member findMember : findMembers) {
            log.debug("findMember: {}", findMember);
            log.debug("findMember.team: {}", findMember.getTeam());
        }
    }

    private void saveTestData() {
        Team teamA = new Team("teamA");
        Team teamB = new Team("teamB");
        em.persist(teamA);
        em.persist(teamB);

        Member member1 = new Member("member1", 10, teamA);
        Member member2 = new Member("member2", 20, teamA);
        Member member3 = new Member("member3", 30, teamB);
        Member member4 = new Member("member4", 40, teamB);
        em.persist(member1);
        em.persist(member2);
        em.persist(member3);
        em.persist(member4);
    }
}