package study.jpa;

import study.jpa.domain.Member;

import javax.persistence.EntityManager;
import javax.persistence.EntityManagerFactory;
import javax.persistence.EntityTransaction;
import javax.persistence.Persistence;

public class DetachMain {
    public static void main(String[] args) {
        EntityManagerFactory emf = Persistence.createEntityManagerFactory("hello");
        EntityManager em = emf.createEntityManager();
        EntityTransaction tx = em.getTransaction();
        tx.begin();

        try {
            System.out.println("find ==================================================");
            Member member1 = em.find(Member.class, 1L);
            member1.setUsername("detach");
            em.detach(member1);

            System.out.println("find ==================================================");
            Member member2 = em.find(Member.class, 1L);
            em.clear();

            System.out.println("find ==================================================");
            Member member3 = em.find(Member.class, 1L);

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
