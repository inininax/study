package study.jpa;

import study.jpa.domain.entity.Member;
import study.jpa.domain.entity.Team;

import javax.persistence.EntityManager;
import javax.persistence.EntityManagerFactory;
import javax.persistence.EntityTransaction;
import javax.persistence.Persistence;

public class EntityMain {
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

            // JPQL - 엔티티 직접 사용
            selectKey(em);
            selectParam(em, member2);
            selectFk(em, team1);

            tx.commit();

        } catch (Exception e) {
            tx.rollback();
            e.printStackTrace();
        } finally {
            em.close();
            emf.close();
        }
    }

    private static void selectKey(EntityManager em) {
        System.out.println("===== selectKey =====");

        // 두 쿼리가 동일함
        em.createQuery("select count(m.id) from Member m")
                .getResultList()
                .forEach(System.out::println);

        em.createQuery("select count(m) from Member m")
                .getResultList()
                .forEach(System.out::println);
    }

    private static void selectParam(EntityManager em, Member member) {
        System.out.println("===== selectParam =====");

        // 두 쿼리가 동일함
        em.createQuery("select m from Member m where m = :member")
                .setParameter("member", member)
                .getResultList()
                .forEach(System.out::println);

        em.createQuery("select m from Member m where m.id = :memberId")
                .setParameter("memberId", member.getId())
                .getResultList()
                .forEach(System.out::println);
    }

    private static void selectFk(EntityManager em, Team team) {
        System.out.println("===== selectFk =====");

        // 두 쿼리가 동일함
        em.createQuery("select m from Member m where m.team = :team")
                .setParameter("team", team)
                .getResultList()
                .forEach(System.out::println);

        em.createQuery("select m from Member m where m.team.id = :teamId")
                .setParameter("teamId", team.getId())
                .getResultList()
                .forEach(System.out::println);
    }

}