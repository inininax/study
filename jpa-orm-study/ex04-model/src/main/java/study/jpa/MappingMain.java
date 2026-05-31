package study.jpa;

import study.jpa.domain.*;

import javax.persistence.EntityManager;
import javax.persistence.EntityManagerFactory;
import javax.persistence.EntityTransaction;
import javax.persistence.Persistence;

public class MappingMain {
    public static void main(String[] args) {
        EntityManagerFactory emf = Persistence.createEntityManagerFactory("hello");
        EntityManager em = emf.createEntityManager();
        EntityTransaction tx = em.getTransaction();
        tx.begin();

        try {
            // 다대일 example
            System.out.println("manyToOneExample ==================================================");
            manyToOneExample(em);

            // 일대다 example
            System.out.println("oneToManyExample ==================================================");
            oneToManyExample(em);

            // 일대일 example
            System.out.println("oneToOneExample ==================================================");
            oneToOneExample(em);

            // 다대다 example
            System.out.println("manyToManyExample ==================================================");
            manyToManyExample(em);

            System.out.println("commit ==================================================");
            tx.commit();

        } catch (Exception e) {
            tx.rollback();
            e.printStackTrace();
        } finally {
            em.close();
            emf.close();
        }
    }

    // N:1 - Member = Owner
    private static void manyToOneExample(EntityManager em) {
        ManyToOneTeam team = new ManyToOneTeam();
        team.setName("N:1");
        em.persist(team);

        ManyToOneMember member = new ManyToOneMember();
        member.setName("N:1");
        member.changeTeam(team); // **
        em.persist(member);

        em.flush();
        // [N:1]
        // 1. insert many_to_one_team
        // 2. insert many_to_one_member
    }

    // 1:N - Team = Owner
    private static void oneToManyExample(EntityManager em) {
        OneToManyMember member = new OneToManyMember();
        member.setName("1:N");
        em.persist(member);

        OneToManyTeam team = new OneToManyTeam();
        team.setName("1:N");
        team.getMembers().add(member);
        em.persist(team);

        em.flush();
        // [1:N] - 가능하면 [N:1]로 구현하는 것을 지향한다.
        // 1. insert one_to_many_member
        // 2. insert one_to_many_team
        // 3. update one_to_many_member
    }

    // 1:1
    private static void oneToOneExample(EntityManager em) {
        /*
        // 객체 중심으로 Owner를 지정 -Member가 Owner일 경우
        OneToOneLocker locker = new OneToOneLocker();
        locker.setName("1:1");
        em.persist(locker);

        OneToOneMember member = new OneToOneMember();
        member.setName("1:1");
        member.changeLocker(locker);
        em.persist(member);
        */

        // 데이터베이스 중심으로 Owner를 지정 - Locker가 Owner일 경우
        OneToOneMember member = new OneToOneMember();
        member.setName("1:1");
        em.persist(member);

        OneToOneLocker locker = new OneToOneLocker();
        locker.setName("1:1");
        locker.changeMember(member);
        em.persist(locker);

        em.flush();
        // [1:1]
        // insert one_to_one_member
        // insert one_to_one_locker
    }

    // N:M
    private static void manyToManyExample(EntityManager em) {
        ManyToManyProduct product = new ManyToManyProduct();
        em.persist(product);

        ManyToManyMember member = new ManyToManyMember();
        member.getProducts().add(product);
        em.persist(member);

        product.getMembers().add(member);

        em.flush();
        // [N:M]
        // insert many_to_many_product
        // insert many_to_many_member
        // insert many_to_many_member_product
    }

}
