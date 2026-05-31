package example.jwt;

import example.jwt.domain.entity.Authority;
import example.jwt.domain.entity.User;
import example.jwt.domain.entity.UserAuthority;
import example.jwt.repository.UserRepository;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Component;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import javax.annotation.PostConstruct;
import javax.persistence.EntityManager;
import java.util.ArrayList;
import java.util.List;
import java.util.Optional;

@Slf4j
@Component
@RequiredArgsConstructor
public class InitDb {

    private final InitService service;

    @PostConstruct
    public void init() {
        service.doInit();
    }

    @Service
    @Transactional
    @RequiredArgsConstructor
    static class InitService {
        private final EntityManager em;
        private final UserRepository userRepository;
        private final PasswordEncoder passwordEncoder;

        public void doInit() {
            Authority authority1 = Authority.create("ROLE_ADMIN", true);
            Authority authority2 = Authority.create("ROLE_USER", true);
            em.persist(authority1);
            em.persist(authority2);

            User user1 = User.create("admin", passwordEncoder.encode("admin"), "admin", true);
            User user2 = User.create("user", passwordEncoder.encode("user"), "user", true);
            em.persist(user1);
            em.persist(user2);

            em.persist(UserAuthority.create(user1, authority1, true));
            em.persist(UserAuthority.create(user1, authority2, true));
            em.persist(UserAuthority.create(user2, authority2, true));

            em.flush();
            em.clear();

            List<User> findUsers = em.createQuery("select distinct u" +
                    " from User as u" +
                    " left join fetch u.userAuthorities as ua" +
                    " left join fetch ua.authority as a" +
                    " order by u.id desc", User.class).getResultList();

            printUsers(findUsers);

            /*log.debug("===== list =====");
            List<UserAuthority> findUserAuthorities = new ArrayList<>(findUsers.get(0).getUserAuthorities());
            log.debug("===== item =====");
            UserAuthority findUserAuthority = findUserAuthorities.get(0);
            log.debug("===== beforeRemove =====");
            findUserAuthority.beforeRemove();
            log.debug("===== remove =====");
            em.remove(findUserAuthority);

            printUsers(findUsers);*/

            Optional<User> findUser = userRepository.findWithEntityGraphByUsername("user");
            log.debug("user: {}", findUser.get());
        }

        private void printUsers(List<User> users) {
            users.forEach(user -> {
                log.debug("user: {}", user);

                user.getUserAuthorities().forEach(userAuthority -> {
                    log.debug("    user.userAuthorities[n]: {}", userAuthority);
                    log.debug("        user.userAuthorities[n].authority: {}", userAuthority.getAuthority());
                });
            });
        }
    }

}
