package study.jpa;

import study.jpa.domain.entity.Member;
import study.jpa.domain.entity.Team;

import javax.persistence.EntityManager;
import javax.persistence.EntityManagerFactory;
import javax.persistence.EntityTransaction;
import javax.persistence.Persistence;

public class NamedQueriesMain {
    public static void main(String[] args) {
        EntityManagerFactory emf = Persistence.createEntityManagerFactory("hello");
        EntityManager em = emf.createEntityManager();
        EntityTransaction tx = em.getTransaction();
        tx.begin();

        try {
            Team team1 = new Team();
            team1.setName("TeamA");
            em.persist(team1);

            Team team2 = new Team();
            team2.setName("TeamB");
            em.persist(team2);

            Member member1 = new Member();
            member1.setUsername("Member1");
            member1.setAge(10);
            member1.changeTeam(team1);
            em.persist(member1);

            Member member2 = new Member();
            member2.setUsername("Member2");
            member2.setAge(15);
            member2.changeTeam(team2);
            em.persist(member2);

            for (int i = 1; i < 3; i++) {
                Member m = new Member();
                m.setUsername("Member" + i);
                m.setAge(20 + i);
                m.changeTeam(team1);
                em.persist(m);
            }

            em.flush();
            em.clear();

            // Named 쿼리 - 정적 쿼리 사용 (동적 쿼리 사용 불가)
            selectNamed1(em);

            tx.commit();

        } catch (Exception e) {
            tx.rollback();
            e.printStackTrace();
        } finally {
            em.close();
            emf.close();
        }
    }

    private static void selectNamed1(EntityManager em) {
        System.out.println("===== selectNamed1 =====");

        em.createNamedQuery("Member.findByUsername", Member.class)
                .setParameter("username", "AAAA")
                .getResultList()
                .forEach(System.out::println);

        Object o = em.createNamedQuery("Member.count")
                .getSingleResult();

        System.out.println(o);
    }

}