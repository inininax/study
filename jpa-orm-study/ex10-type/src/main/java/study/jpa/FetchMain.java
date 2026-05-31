package study.jpa;

import study.jpa.domain.lazy.Locker;
import study.jpa.domain.lazy.Member;
import study.jpa.domain.lazy.Team;

import javax.persistence.EntityManager;
import javax.persistence.EntityManagerFactory;
import javax.persistence.EntityTransaction;
import javax.persistence.Persistence;
import java.util.List;

public class FetchMain {
    public static void main(String[] args) {
        EntityManagerFactory emf = Persistence.createEntityManagerFactory("hello");
        EntityManager em = emf.createEntityManager();
        EntityTransaction tx = em.getTransaction();
        tx.begin();

        try {
            Team team = new Team();
            team.setName("Team A");
            em.persist(team);

            Member member = new Member();
            member.setName("Member A");
            member.changeTeam(team);
            em.persist(member);

            Locker locker = new Locker();
            locker.setName("Locker A");
            locker.changeMember(member);
            em.persist(locker);

            em.flush();
            em.clear();

            System.out.println("==========");

            Member findMember = em.find(Member.class, member.getId()); // select member
            System.out.println("member.name=" + findMember.getName());
            System.out.println("member.locker=" + findMember.getLocker().getName());
            System.out.println("team.name=" + findMember.getTeam().getName()); // select team

            em.flush();
            em.clear();

            System.out.println("==========");

            Locker findLocker = em.find(Locker.class, locker.getId());
            System.out.println("locker.name=" + findLocker.getName());
            System.out.println("locker.name=" + findLocker.getMember().getName());

            System.out.println("==========");

            // **
            // SQL: select * from member 조회 후
            // team이 EAGER 면 조회 후 바로 select 문이 list 만큼 호출 됨
            List<Member> members = em.createQuery("select m from lazy_member m", Member.class)
                    .getResultList();

            members.forEach(System.out::println);

            tx.commit();

        } catch (Exception e) {
            tx.rollback();
            e.printStackTrace();
        } finally {
            em.close();
            emf.close();
        }
    }
}
