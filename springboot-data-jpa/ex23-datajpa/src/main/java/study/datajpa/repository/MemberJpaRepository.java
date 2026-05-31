package study.datajpa.repository;

import org.springframework.stereotype.Repository;
import study.datajpa.entity.Member;

import javax.persistence.EntityManager;
import javax.persistence.PersistenceContext;
import java.util.List;
import java.util.Optional;

/**
 * https://docs.spring.io/spring-data/jpa/docs/current/reference/html/#jpa.query-methods.query-creation
 * https://docs.spring.io/spring-data/jpa/docs/current/reference/html/#repositories.query-methods.query-creation
 * https://docs.spring.io/spring-data/jpa/docs/current/reference/html/#repositories.limit-query-result
 */
@Repository
public class MemberJpaRepository {

    @PersistenceContext
    private EntityManager em;

    public Member save(Member member) {
        em.persist(member);
        return member;
    }

    public void delete(Member member) {
        em.remove(member);
    }

    public List<Member> findAll() {
        return em.createQuery("select m from Member m", Member.class)
                .getResultList();
    }

    public Optional<Member> findById(Long id) {
        Member member = em.find(Member.class, id);
        return Optional.ofNullable(member);
    }

    public long count() {
        return em.createQuery("select count(m) from Member m", Long.class)
                .getSingleResult();
    }

    public Member find(Long id) {
        return em.find(Member.class, id);
    }

    public List<Member> findByUsernameAndAgeGreaterThan(String username, int age) {
        return em.createQuery(
                "select m " +
                        " from Member m " +
                        " where m.username = :username " +
                        " and m.age > :age ", Member.class)
                .setParameter("username", username)
                .setParameter("age", age)
                .getResultList();
    }

    //Named Query - @Query 생략 가능 (Named 쿼리, 실무에서는 잘 사용하지 않음) - Named Query 사용 시 @Param 필요함
    public List<Member> findByUsername(String username) {
        return em.createNamedQuery("Member.findByUsername", Member.class)
                .setParameter("username", username)
                .getResultList();
    }

    //select m from Member m where m.age = :age order by m.username desc
    //
    //select member0_.member_id as member_i1_0_, member0_.age as age2_0_, member0_.team_id as team_id4_0_, member0_.username as username3_0_
    //rom member member0_
    //where member0_.age=?
    //order by member0_.username desc
    //limit ?
    public List<Member> findByPage(int age, int offset, int limit) {
        return em.createQuery(
                "select m" +
                        " from Member m" +
                        " where m.age = :age" +
                        " order by m.username desc", Member.class)
                .setParameter("age", age)
                .setFirstResult(offset)
                .setMaxResults(limit)
                .getResultList();
    }

    //select count(m) from Member m where m.age = :age
    //
    //select count(member0_.member_id) as col_0_0_
    //from member member0_
    //where member0_.age=?
    public long totalCount(int age) {
        return em.createQuery(
                "select count(m)" +
                        " from Member m" +
                        " where m.age = :age", Long.class)
                .setParameter("age", age)
                .getSingleResult();
    }

    public int bulkAgePlus(int age) {
        int resultCount = em.createQuery(
                "update Member m" +
                        " set m.age = m.age + 1" +
                        " where m.age >= :age")
                .setParameter("age", age)
                .executeUpdate();
        return resultCount;
    }

}

