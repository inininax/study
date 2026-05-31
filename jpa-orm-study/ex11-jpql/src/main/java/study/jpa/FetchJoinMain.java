package study.jpa;

import study.jpa.domain.entity.Member;
import study.jpa.domain.entity.Team;

import javax.persistence.EntityManager;
import javax.persistence.EntityManagerFactory;
import javax.persistence.EntityTransaction;
import javax.persistence.Persistence;
import java.util.List;

public class FetchJoinMain {
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

            /*
             * Fetch Join
             * SQL 조인 종류 X
             * JPQL에서 성능 최적화를 위해 제공하는 기능
             * 연관된 Entity나 Collection을 SQL 한번에 함께 조회하는 기능
             * join fetch 명령어 사용
             * fetch join ::= LEFT [OUTER] JOIN, INNER JOIN FETCH 조인 경로
             */
            select8fetch(em);
            select9collectionFetchAndTeamBatchSize(em);
            select10distinctCollectionFetch(em);

            /*
             * <fetch join의 한계>
             * 페치 조인 대상에는 별칭을 줄 수 없다.
             *      하이버네이트는 가능하지만 사용하지 말 것
             *
             * 둘 이상의 컬렉션은 페치 조인할 수 없다.
             *
             * 컬렉션을 페치 조인하면 페이징 API를 사용할 수 없다.
             *      !! sql 기준으로 가져온 후 페이징 하기 때문에 원하는 결과가 나올 수 없음 (팀에 속한 맴버가 한명만 나온다던가...)
             *      일대일, 다대일 같은 단일 값 연관 필드들은 패치 조인해도 페이징 가능
             *      하이버네이트는 경고 로그를 남기고 메모리에서 페이징 (매우 위험)
             *
             * 여러 테이블을 조인해서 엔티티가 가진 모양이 아닌 전혀 다른 결과를 내야하면 페치 조인 보다는 일반 조인을 사용하고
             * 필요한 데이터만 불러와 DTO로 반환하는 것이 효과적이다.
             */

            tx.commit();

        } catch (Exception e) {
            tx.rollback();
            e.printStackTrace();
        } finally {
            em.close();
            emf.close();
        }
    }

    // 연관 fetch join
    private static void select8fetch(EntityManager em) {
        // 회원을 조회하면서 연관된 팀도 함께 조회 (한방 쿼리)

        // select m from Member m inner join fetch m.team
        // -> select m.*, t.* from Member m inner join Team t on (m.team_id = t.id)

        //    /* select m from Member m join fetch m.team */
        //    select
        //        member0_.member_id as member_i1_6_0_,
        //        team1_.team_id as team_id1_9_1_,
        //        member0_.city as city2_6_0_,
        //        member0_.street as street3_6_0_,
        //        member0_.zipcode as zipcode4_6_0_,
        //        member0_.age as age5_6_0_,
        //        member0_.team_id as team_id7_6_0_,
        //        member0_.username as username6_6_0_,
        //        team1_.name as name2_9_1_
        //    from Member member0_
        //    inner join Team team1_ on member0_.team_id=team1_.team_id
        System.out.println("===== select8fetch =====");
        List<Member> members = em.createQuery("select m from Member m join fetch m.team", Member.class)
                .getResultList();
        members.forEach(member -> {
            System.out.println("username=" + member.getUsername() + ", team.name=" + member.getTeam().getName());
        });
    }

    // collection fetch join (중복 데이터 존재)
    private static void select9collectionFetchAndTeamBatchSize(EntityManager em) {
        // select t from Team t join fetch t.members where t.name = 'TeamA'
        // -> select t.*, m.* from team t inner join member m on t.id = m.team_id where t.name = 'TeamA'

        //    /* select t From Team t join t.members where t.name = 'TeamA' */
        //    select
        //        team0_.team_id as team_id1_9_,
        //        team0_.name as name2_9_
        //    from Team team0_
        //    inner join Member members1_ on team0_.team_id=members1_.team_id
        //    where team0_.name='TeamA'
        //
        //    1 + n
        System.out.println("===== select9collectionFetchAndTeamBatchSize =====");

        String query = "select t From Team t join t.members where t.name = 'TeamA'";

        // public class Team {
        //      @BatchSize(size = 1000)
        //      @OneToMany(mappedBy = "team")
        //      private List<Member> members = new ArrayList<>();
        // }
        //
        // 01. select t.* from team t
        // 02. select m.* from member m where m.team_id in ( ? , ? )
        //
        // 위와 같은 방법으로 batch size 같이 실행하여 loop 별 쿼리 실행을 방지함

        List<Team> teams = em.createQuery(query, Team.class)
                .getResultList();

        teams.forEach(team -> {
            System.out.println("id=" + team.getId() + ",name=" + team.getName() + ", members.size=" + team.getMembers().size());
            team.getMembers().forEach(member -> {
                System.out.println("-> id=" + member.getId() + ", username=" + member.getUsername() + ", team.name=" + member.getTeam().getName());
            });
        });
    }

    // collection fetch join (중복 제거)
    private static void select10distinctCollectionFetch(EntityManager em) {
        System.out.println("===== select10distinctCollectionFetch =====");

        // distinct , fetch
        List<Team> teams = em.createQuery("select distinct t from Team t join fetch t.members", Team.class)
                .getResultList();

        System.out.println("teams size=" + teams.size());

        // fetch가 없으면 getMembers() 시 마다 각각의 쿼리를 실행
        for (Team team : teams) {
            System.out.println("team id=" + team.getId() + ",name=" + team.getName() + ", members.size=" + team.getMembers().size());
            for (Member member : team.getMembers()) {
                System.out.println("-> members id=" + member.getId() + ", username=" + member.getUsername() + ", team.name=" + member.getTeam().getName());
            }
        }
    }

}