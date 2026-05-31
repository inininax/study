package study.jpa;

import study.jpa.domain.Member;
import study.jpa.domain.RoleType;

import javax.persistence.EntityManager;
import javax.persistence.EntityManagerFactory;
import javax.persistence.EntityTransaction;
import javax.persistence.Persistence;
import java.time.LocalDate;
import java.time.LocalDateTime;
import java.util.Date;

public class LazyMain {
    public static void main(String[] args) {
        EntityManagerFactory emf = Persistence.createEntityManagerFactory("hello");
        EntityManager em = emf.createEntityManager();
        EntityTransaction tx = em.getTransaction();
        tx.begin();

        try {
            Member member1 = new Member();
            Member member2 = new Member();

            member1.setUsername("A");
            member1.setRoleType(RoleType.USER);
            member1.setCreateDate(new Date());
            member1.setLastModifiedDate(new Date());
            member1.setTestLocalDate(LocalDate.now());
            member1.setTestLocalDateTime(LocalDateTime.now());

            member2.setUsername("B");
            member2.setRoleType(RoleType.ADMIN);

            System.out.println("persist ==================================================");
            em.persist(member1);

            System.out.println("persist ==================================================");
            em.persist(member2);

            System.out.println(member1.getUsername());
            System.out.println(member2.getUsername());

            // 영속 엔티티 조회
            System.out.println("find ==================================================");
            Member member3 = em.find(Member.class, 105L);

            // 영속 엔티티 변경 감지
            if (member3 != null) {
                member3.setUsername("A1");
            }

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
