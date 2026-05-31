package study.datajpa;

import com.querydsl.jpa.JPQLQueryFactory;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Component;
import org.springframework.transaction.annotation.Transactional;
import study.datajpa.domain.dto.UserCmd;
import study.datajpa.domain.entity.Post;
import study.datajpa.domain.entity.User;
import study.datajpa.repository.PostRepository;
import study.datajpa.repository.UserRepository;

import javax.annotation.PostConstruct;
import javax.persistence.EntityManager;

@Slf4j
@Component
@RequiredArgsConstructor
public class InitDB {
    private final InitService service;

    @PostConstruct
    private void init() {
        log.debug("InitDB init");
        service.master();
        service.update();
        service.slave();
    }

    @Slf4j
    @Component
    @Transactional(rollbackFor = Exception.class)
    @RequiredArgsConstructor
    static class InitService {
        private final EntityManager em;
        private final JPQLQueryFactory queryFactory;
        private final UserRepository userRepository;
        private final PostRepository postRepository;

        public void master() {
            userRepository.save(User.create("master" + (long) (Math.random() * 1000 + 1)));
            userRepository.save(User.create("master" + (long) (Math.random() * 1000 + 1)));
            postRepository.save(Post.create("title" + (long) (Math.random() * 1000 + 1), "contents"));
        }

        public void update() {
            userRepository.save(User.create("master" + (long) (Math.random() * 1000 + 1)));
            postRepository.save(Post.create("title" + (long) (Math.random() * 1000 + 1), "contents"));
        }

        @Transactional(readOnly = true)
        public void slave() {
            log.debug("slave user count : {}", userRepository.count());
            log.debug("slave user list  : {}", userRepository.findAll());
            log.debug("slave user list  : {}", userRepository.findAllByCmd(UserCmd.builder().email("slave").build()));
        }
    }
}
