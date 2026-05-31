package example.jwt.repository;

import example.jwt.domain.entity.User;
import org.springframework.data.jpa.repository.EntityGraph;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.Optional;

@Repository
public interface UserRepository extends JpaRepository<User, Long> {

    /*
        select
            user0_.user_id as user_id1_1_0_,
            userauthor1_.authority_id as authorit1_2_1_,
            userauthor1_.user_id as user_id2_2_1_,
            authority2_.authority_id as authorit1_0_2_,
            user0_.created_date as created_2_1_0_,
            user0_.last_modified_date as last_mod3_1_0_,
            user0_.created_by as created_4_1_0_,
            user0_.last_modified_by as last_mod5_1_0_,
            user0_.activated as activate6_1_0_,
            user0_.name as name7_1_0_,
            user0_.password as password8_1_0_,
            user0_.username as username9_1_0_,
            userauthor1_.created_date as created_3_2_1_,
            userauthor1_.last_modified_date as last_mod4_2_1_,
            userauthor1_.created_by as created_5_2_1_,
            userauthor1_.last_modified_by as last_mod6_2_1_,
            userauthor1_.activated as activate7_2_1_,
            userauthor1_.user_id as user_id2_2_0__,
            userauthor1_.authority_id as authorit1_2_0__,
            authority2_.created_date as created_2_0_2_,
            authority2_.last_modified_date as last_mod3_0_2_,
            authority2_.created_by as created_4_0_2_,
            authority2_.last_modified_by as last_mod5_0_2_,
            authority2_.activated as activate6_0_2_,
            authority2_.name as name7_0_2_
        from user user0_
        left outer join user_authority userauthor1_ on user0_.user_id            = userauthor1_.user_id
        left outer join authority       authority2_ on userauthor1_.authority_id = authority2_.authority_id
        where user0_.username = ?
    */
    @EntityGraph(attributePaths = {"userAuthorities", "userAuthorities.authority"})
    Optional<User> findWithEntityGraphByUsername(String username);

}
