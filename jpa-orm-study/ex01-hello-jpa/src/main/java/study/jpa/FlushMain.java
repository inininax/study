package study.jpa;

import study.jpa.domain.Member;

import javax.persistence.EntityManager;
import javax.persistence.EntityManagerFactory;
import javax.persistence.EntityTransaction;
import javax.persistence.Persistence;
import java.util.List;

public class FlushMain {
    public static void main(String[] args) {
        EntityManagerFactory emf = Persistence.createEntityManagerFactory("hello");
        EntityManager em = emf.createEntityManager();
        EntityTransaction tx = em.getTransaction();
        tx.begin();

        try {
            Member member1 = new Member();
            member1.setUsername("A");

            Member member2 = new Member();
            member2.setUsername("B");

            Member member3 = new Member();
            member3.setUsername("C");

            System.out.println("persist ==================================================");
            em.persist(member1);

            System.out.println("flush ==================================================");
            em.flush();

            System.out.println("persist ==================================================");
            em.persist(member2);

            System.out.println("persist ==================================================");
            em.persist(member3);

            // 강제 flush
            System.out.println("createQuery ==================================================");
            List<Member> members = em.createQuery("select m from Member m", Member.class)
                    .getResultList();

            members.forEach(m -> System.out.println("Member = " + m.toString()));

            System.out.println("commit ==================================================");
            tx.commit(); // flush -> 1차 캐시(entity <> snapshot) 비교 -> update
        } catch (Exception e) {
            tx.rollback();
            e.printStackTrace();
        } finally {
            em.close();
            emf.close();
        }
    }
}
