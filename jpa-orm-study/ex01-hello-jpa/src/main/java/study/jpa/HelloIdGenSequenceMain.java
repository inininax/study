package study.jpa;

import study.jpa.domain.MemberSequence;

import javax.persistence.EntityManager;
import javax.persistence.EntityManagerFactory;
import javax.persistence.EntityTransaction;
import javax.persistence.Persistence;
import java.util.List;

public class HelloIdGenSequenceMain {
    public static void main(String[] args) {
        EntityManagerFactory emf = Persistence.createEntityManagerFactory("hello");
        EntityManager em = emf.createEntityManager();
        EntityTransaction tx = em.getTransaction();
        tx.begin();

        try {
            MemberSequence member = new MemberSequence();
            //member.setId(1L);
            member.setUsername("Name1");

            System.out.println("persist ==================================================");
            em.persist(member);
            // none sql => insert sql (GenerationType.IDENTITY)
            // none sql => select nextval(..xxx..) sql (GenerationType.SEQUENCE)

            System.out.println("find ==================================================");
            MemberSequence findMember = em.find(MemberSequence.class, 1L);
            // none sql => none sql (GenerationType.IDENTITY)
            // none sql => none sql (GenerationType.SEQUENCE)

            System.out.println("member == findMember 1 : " + (member == findMember)); // true

            if (findMember != null) {
                findMember.setUsername("Name2");
                member.setUsername("Name3");

                System.out.println("member == findMember 2 : " + (member == findMember)); // true
                System.out.println("member     : " + member.getUsername()); // HelloC3
                System.out.println("findMember : " + findMember.getUsername()); // HelloC3
            }

            System.out.println("createQuery ==================================================");
            // insert + select sql => select sql (GenerationType.IDENTITY)              ########## update not working ##########
            // insert + select sql => insert + select sql (GenerationType.SEQUENCE)     ########## insert 되는데 Name1로 insert 됨 ##########
            List<MemberSequence> members = em.createQuery("select m from MemberSequence as m", MemberSequence.class)
                    .setFirstResult(0)
                    .setMaxResults(10)
                    .getResultList();

            members.forEach(m -> System.out.println("MemberSequence - id: " + m.getId() + ", name: " + m.getUsername()));
            // MemberSequence - id: 1, name: Name3 (GenerationType.IDENTITY) ########## update not working ##########
            // MemberSequence - id: 1, name: Name3 (GenerationType.SEQUENCE)

            // throw new Exception("rollback test");

            System.out.println("commit ==================================================");
            tx.commit(); // none sql

            System.out.println("end ==================================================");

        } catch (Exception e) {
            System.out.println("rollback");
            tx.rollback();
            e.printStackTrace();
        } finally {
            em.close();
        }
        emf.close();
    }
}
