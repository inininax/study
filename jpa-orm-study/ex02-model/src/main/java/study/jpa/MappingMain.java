package study.jpa;

import study.jpa.domain.Member;
import study.jpa.domain.Team;

import javax.persistence.EntityManager;
import javax.persistence.EntityManagerFactory;
import javax.persistence.EntityTransaction;
import javax.persistence.Persistence;
import java.util.List;

public class MappingMain {
    public static void main(String[] args) {
        EntityManagerFactory emf = Persistence.createEntityManagerFactory("hello");
        EntityManager em = emf.createEntityManager();
        EntityTransaction tx = em.getTransaction();
        tx.begin();

        try {
            Team team = new Team();
            team.setName("jpa");
            System.out.println("persist team ==================================================");
            em.persist(team); // select nextval(hibernate_sequence); sql

            Member member = new Member();
            member.setName("hello");

            // ** 중요
            // member.setTeam(team);
            // team.getMembers().add(member);
            member.changeTeam(team);

            System.out.println("persist member ==================================================");
            em.persist(member); // select nextval(hibernate_sequence); sql

            //em.flush();

            System.out.println("findMember em.find ==================================================");
            Member findMember = em.find(Member.class, member.getId()); // none sql

            if (findMember != null) {
                System.out.println(findMember.getName());

                System.out.println("findMember.getTeam() ==================================================");
                Team findTeam = findMember.getTeam(); // none sql

                if (findTeam != null) {
                    System.out.println(findTeam.getName());
                }
            }

            System.out.println("findTeam em.find ==================================================");
            Team findTeam = em.find(Team.class, team.getId()); // none sql

            if (findTeam != null) {
                System.out.println(findTeam.getName());

                System.out.println("findTeam.getMembers() ==================================================");
                List<Member> members = findTeam.getMembers(); // none sql
                if (members != null) {
                    members.forEach(m -> System.out.println(m.getName()));
                }
            }

            System.out.println("commit ==================================================");
            tx.commit(); // insert + insert sql

        } catch (Exception e) {
            tx.rollback();
            e.printStackTrace();
        } finally {
            em.close();
            emf.close();
        }
    }
}
