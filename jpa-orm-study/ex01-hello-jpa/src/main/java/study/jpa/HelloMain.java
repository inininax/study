package study.jpa;

import study.jpa.domain.Member;

import javax.persistence.EntityManager;
import javax.persistence.EntityManagerFactory;
import javax.persistence.EntityTransaction;
import javax.persistence.Persistence;
import java.util.List;

public class HelloMain {
    public static void main(String[] args) {
        EntityManagerFactory emf = Persistence.createEntityManagerFactory("hello");
        EntityManager em = emf.createEntityManager();
        EntityTransaction tx = em.getTransaction();
        tx.begin();

        try {
            Member member = new Member();
            member.setId(1L);
            member.setUsername("HelloC");

            System.out.println("persist ==================================================");
            em.persist(member); // none sql

            System.out.println("find ==================================================");
            Member findMember = em.find(Member.class, 1L); // none sql

            System.out.println(member == findMember);

            if (findMember != null) findMember.setUsername("HelloC3");

            System.out.println("createQuery ==================================================");
            List<Member> members = em.createQuery("select m from Member as m", Member.class) // insert + select sql
                    .setFirstResult(5)
                    .setMaxResults(8)
                    .getResultList();

            members.forEach(m -> System.out.println("Member.name = " + m.getUsername()));

            // throw new Exception("rollback test");

            System.out.println("commit ==================================================");
            tx.commit(); // none sql
        } catch (Exception e) {
            System.out.println("rollback");
            tx.rollback();
            e.printStackTrace();
        } finally {
            em.close();
            emf.close();
        }
    }
}
