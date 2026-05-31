package study.jpa;

import study.jpa.domain.entity.Member;
import study.jpa.domain.entity.Team;

import javax.persistence.EntityManager;
import javax.persistence.EntityManagerFactory;
import javax.persistence.EntityTransaction;
import javax.persistence.Persistence;

public class ExecuteMain {
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

            // JPQL - 벌크 연산
            // 벌크 연산 후 반드시 clear하여 영속성 컨텍스트 초기화를 실행한다.
            update(em);

            tx.commit();

        } catch (Exception e) {
            tx.rollback();
            e.printStackTrace();
        } finally {
            em.close();
            emf.close();
        }
    }

    private static void update(EntityManager em) {
        System.out.println("===== update =====");

        //    update Product p
        //       set p.price = p.price * 1.1
        //     where p.stockAmount < :stockAmount
        //
        //    update Product
        //       set price=price*1.1
        //     where stockAmount < ?
        String query = "update Product p set p.price = p.price * 1.1 where p.stockAmount < :stockAmount";
        int resultCount = em.createQuery(query)
                .setParameter("stockAmount", 10)
                .executeUpdate();
        System.out.println(resultCount);

        // update Member m set m.age = :age
        // update Member set age = ?
        query = "update Member m set m.age = :age";
        resultCount = em.createQuery(query)
                .setParameter("age", 20)
                .executeUpdate();
        System.out.println(resultCount);

        // 벌크 연산 후 반드시 clear하여 영속성 컨텍스트 초기화를 실행한다.
        em.flush();
        em.clear();
    }

}