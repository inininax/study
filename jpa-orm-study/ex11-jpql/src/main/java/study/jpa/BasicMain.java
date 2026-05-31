package study.jpa;

import study.jpa.domain.dto.MemberDto;
import study.jpa.domain.entity.Member;
import study.jpa.domain.entity.Order;
import study.jpa.domain.entity.Team;

import javax.persistence.*;
import java.util.Collection;
import java.util.List;

public class BasicMain {
    public static void main(String[] args) {
        EntityManagerFactory emf = Persistence.createEntityManagerFactory("hello");
        EntityManager em = emf.createEntityManager();
        EntityTransaction tx = em.getTransaction();
        tx.begin();

        try {
            Team team = new Team();
            team.setName("A");
            em.persist(team);

            Member member = new Member();
            member.setUsername("A");
            member.setAge(10);
            member.changeTeam(team);
            em.persist(member);

            for (int i = 1; i < 100; i++) {
                Member m = new Member();
                m.setUsername("Member" + i);
                m.setAge(20 + i);
                m.changeTeam(team);
                em.persist(m);
            }

            em.flush();
            em.clear();

            select1singleAndList(em); // single, list
            select2(em); // 명시적, 묵시적
            select3dto(em); // 프로젝션 - 여러 값 조회
            select4paging(em); // 페이징
            select5innerJoin(em); // inner join
            select5leftJoin(em); // left join
            select5crossJoin(em); // cross join
            select6subQuery(em);
            select7field(em);

            tx.commit();

        } catch (Exception e) {
            tx.rollback();
            e.printStackTrace();
        } finally {
            em.close();
            emf.close();
        }
    }

    private static void select1singleAndList(EntityManager em) {
        try {
            System.out.println("===== getSingleResult =====");
            Member findMember = em.createQuery("select m from Member as m where m.username = :username", Member.class)
                    .setParameter("username", "Member1")
                    .getSingleResult();
            System.out.println("Member.username=" + findMember.getUsername());
        } catch (NoResultException e1) {
            e1.printStackTrace();
        } catch (NonUniqueResultException e2) {
            e2.printStackTrace();
        }

        System.out.println("===== getResultList =====");
        List<Member> findMembers = em.createQuery("select m from Member as m where m.age > :age order by m.age desc", Member.class)
                .setParameter("age", 10)
                .setFirstResult(0)
                .setMaxResults(20)
                .getResultList();
        findMembers.forEach(System.out::println);
    }

    private static void select2(EntityManager em) {
        // 묵시적
        System.out.println("===== select2 1 =====");
        List<Team> teams1 = em.createQuery("select m.team from Member m", Team.class).getResultList();
        teams1.forEach(System.out::println);

        // 명시적
        System.out.println("===== select2 2 =====");
        List<Team> teams2 = em.createQuery("select t from Member m join m.team t", Team.class).getResultList();
        teams2.forEach(System.out::println);
    }

    private static void select3dto(EntityManager em) {
        System.out.println("select3dto 1");
        List<Object[]> list1 = em.createQuery("select m.username, m.age from Member m")
                .getResultList();
        list1.forEach(result -> {
            System.out.format("username=%s,age=%d\n", result[0], result[1]);
        });

        System.out.println("===== select3dto 2 =====");
        List<MemberDto> list2 = em.createQuery("select new study.jpa.domain.dto.MemberDto(m.username, m.age) from Member m")
                .getResultList();
        list2.forEach(System.out::println);
    }

    private static void select4paging(EntityManager em) {
        System.out.println("===== select4paging 1 =====");
        List<Member> findMembers = em.createQuery("select m from Member as m where m.age > :age order by m.age desc", Member.class)
                .setParameter("age", 0)
                .setFirstResult(1)
                .setMaxResults(3)
                .getResultList();
        findMembers.forEach(System.out::println);
    }

    private static void select5innerJoin(EntityManager em) {
        System.out.println("===== select5innerJoin 1 =====");
        // from Member member0_
        // inner join Team team1_ on member0_.team_id=team1_.team_id and (team1_.name='A')
        String query = "select m from Member m join m.team t on t.name = 'A'";
        List<Member> list = em.createQuery(query, Member.class)
                .setFirstResult(10)
                .setMaxResults(5)
                .getResultList();
        list.forEach(System.out::println);

        System.out.println("===== select5innerJoin 2 =====");
        // from Member member0_
        // inner join Team team1_ on (member0_.team_id=team1_.team_id and team1_.name='A')
        query = "select m from Member m join Team t on (m.team = t and t.name = 'A')";
        list = em.createQuery(query, Member.class)
                .setFirstResult(10)
                .setMaxResults(5)
                .getResultList();
        list.forEach(System.out::println);

        // 사용 금지 cross join으로 처리됨
        // from Member member0_
        // cross join Team team1_
        // where member0_.team_id=team1_.team_id and team1_.name='A'
        // System.out.println("inner join 3");
        // query1 = "select m from Member m, Team t where m.team = t and t.name = 'A'";
    }

    private static void select5leftJoin(EntityManager em) {
        System.out.println("===== select5leftJoin 1 =====");
        // from Member member0_
        // left outer join Team team1_ on member0_.team_id=team1_.team_id and (team1_.name='A')
        String query = "select m from Member m left join m.team t on t.name = 'A'";
        List<Member> list = em.createQuery(query, Member.class)
                .setFirstResult(10)
                .setMaxResults(5)
                .getResultList();
        list.forEach(System.out::println);

        System.out.println("===== select5leftJoin 2 - 조인 대상 필터링 =====");
        // from Member member0_
        // left outer join Team team1_ on (member0_.team_id=team1_.team_id and team1_.name='A')
        query = "select m from Member m left join Team t on (m.team = t and t.name = 'A')";
        list = em.createQuery(query, Member.class)
                .setFirstResult(10)
                .setMaxResults(5)
                .getResultList();
        list.forEach(System.out::println);

        System.out.println("===== select5leftJoin 3 - 연관 관계가 없는 엔티티 외부 조인 =====");
        // from Member member0_
        // left outer join Team team1_ on (member0_.username=team1_.name)
        query = "select m from Member m left join Team t on (m.username = t.name)";
        list = em.createQuery(query, Member.class)
                .setFirstResult(10)
                .setMaxResults(5)
                .getResultList();
        list.forEach(System.out::println);
    }

    private static void select5crossJoin(EntityManager em) {
        System.out.println("===== select5crossJoin 1 =====");
        // from Member member0_
        // cross join Team team1_
        // where member0_.username = team1_.name
        String query = "select m from Member m, Team t where m.username = t.name";
        List<Member> list = em.createQuery(query, Member.class)
                .setFirstResult(10)
                .setMaxResults(5)
                .getResultList();
        list.forEach(System.out::println);
    }

    private static void select6subQuery(EntityManager em) {
        System.out.println("===== select6subQuery 1 =====");
        // from Member member0_
        // where member0_.age > ( select avg(member1_.age) from Member member1_ )
        em.createQuery("select m from Member m where m.age > (select avg(m2.age) from Member m2)", Member.class)
                .setFirstResult(0)
                .setMaxResults(5)
                .getResultList().forEach(System.out::println);

        System.out.println("===== select6subQuery 2 =====");
        // from Member member0_
        // where (
        //    select count(order1_.order_id)
        //    from Orders order1_
        //    where member0_.member_id=order1_.member_id
        // ) > 0
        em.createQuery("select m from Member m where (select count(o) from Orders o where m = o.member) > 0", Member.class)
                .setFirstResult(0)
                .setMaxResults(3)
                .getResultList().forEach(System.out::println);

        // [NOT] EXISTS (subquery): 서브쿼리에 결과가 존재하면 참
        //      {ALL | ANY | SOME} (subquery)
        //      ALL 모두 만족하면 참
        //      ANY, SOME: 같은 의미, 조건을 하나라도 만족하면 참
        // [NOT] IN (subquery): 서브쿼리의 결과 중 하나라도 같은 것이 있으면 참

        em.createQuery("select m from Member m where exists ( select t from m.team t where t.name = 'A' )", Member.class)
                .setFirstResult(0)
                .setMaxResults(3)
                .getResultList()
                .forEach(System.out::println);

        em.createQuery("select o from Orders o where o.orderAmount > ALL( select p.stockAmount from Product p )", Order.class)
                .setFirstResult(0)
                .setMaxResults(3)
                .getResultList()
                .forEach(System.out::println);

        em.createQuery("select m from Member m where m.team = ANY( select t from Team t )", Member.class)
                .setFirstResult(0)
                .setMaxResults(3)
                .getResultList()
                .forEach(System.out::println);

        // JPA는 WHERE, HAVING 절에서만 서브 쿼리 사용 가능
        // SELECT 절도 가능(하이버네이트에서 지원)
        // FROM 절의 서브 쿼리는 현재 JPQL에서 불가능
        //      조인으로풀수있으면풀어서해결
    }

    private static void select7field(EntityManager em) {
        // 01. 상태 필드 (state field: 경로 탐색의 끝)
        System.out.println("===== 01. 상태 필드 (state field: 경로 탐색의 끝) =====");
        List<String> list1 = em.createQuery("select m.username from Member m", String.class)
                .setFirstResult(0)
                .setMaxResults(3)
                .getResultList();
        list1.forEach(System.out::println);

        System.out.println("===== 02.01. 단일 값 연관 경로: @ManyToOne, @OneToOne 등 묵시적 조인 (inner join) 발생, 탐색 O =====");
        // 02. 단일 값 연관 경로: @ManyToOne, @OneToOne 등 묵시적 조인 (inner join) 발생, 탐색 가능
        //
        // select m.team from Member m
        // select t from Member m join m.team t
        //
        // 묵시적 조인 발생
        // from Member member0_
        // inner join Team team1_ on member0_.team_id=team1_.team_id
        em.createQuery("select m.team from Member m", Team.class)
                .setFirstResult(0)
                .setMaxResults(3)
                .getResultList()
                .forEach(System.out::println);

        System.out.println("===== 02.02. 단일 값 연관 경로: @ManyToOne, @OneToOne 등 묵시적 조인 (inner join) 발생, 탐색 O =====");
        // 묵시적 조인을 명시적으로 표기
        // from Member member0_
        // inner join Team team1_ on member0_.team_id=team1_.team_id
        em.createQuery("select t from Member m join m.team t", Team.class)
                .setFirstResult(0)
                .setMaxResults(3)
                .getResultList()
                .forEach(System.out::println);

        // 03. 컬랙션 값 연관 경로: @OneToMany, @ManyToMany 등 묵시적 내부 조인 발생, 탐색 불가
        System.out.println("===== 03. 컬랙션 값 연관 경로: @OneToMany, @ManyToMany 등 묵시적 내부 조인 발생, 탐색 불가 =====");
        // from Team team0_
        // inner join Member members1_ on team0_.team_id=members1_.team_id
        //
        // collection을 응답하기 때문에 경로 탐색이 불가능하다.
        Collection list2 = em.createQuery("select t.members from Team t", Collection.class)
                .setFirstResult(0)
                .setMaxResults(5)
                .getResultList();
        for (Object o : list2) {
            System.out.println("o = " + o);
        }

        // size와 같은 함수들은 사용 가능:
        //      select (select count(members1_.team_id) from Member members1_ where team0_.team_id=members1_.team_id) as col_0_0_
        //      from Team team0_ limit ?
        em.createQuery("select t.members.size from Team t", Integer.class)
                .setFirstResult(0)
                .setMaxResults(5)
                .getResultList()
                .forEach(System.out::println);

        // 경로 탐색을 위해서는 명시적인 조인을 사용해야 한다.
        //      select members1_.username as col_0_0_
        //      from Team team0_
        //      inner join Member members1_ on team0_.team_id=members1_.team_id
        em.createQuery("select m.username from Team t join t.members m", String.class)
                .setFirstResult(0)
                .setMaxResults(5)
                .getResultList()
                .forEach(System.out::println);

        // 결론 명시적 조인만 사용하자.
        // 묵시적 조인은 항상 내부 조인인다. inner join
        // 명시적 조인을 통해 별칭을 줘서 경로 탐색이 가능하다.

        // select o.member.team      from Order o                   -> 성공 member에서 경로 탐색 가능
        // select t.members          from Team  t                   -> 성공 , 경로 탐색 불가
        // select t.members.username from Team  t                   -> 실패 컬랙션 타입은 경로 탐색 불가능
        // select m.username         from Team  t join t.members m  -> 성공 , 명시적 조인은 경로 탐색 가능
    }

}