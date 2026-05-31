package study.datajpa.repository;

import lombok.extern.slf4j.Slf4j;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.annotation.Rollback;
import org.springframework.transaction.annotation.Transactional;
import study.datajpa.domain.entity.Post;

import static org.assertj.core.api.Assertions.assertThat;

@Slf4j
@SpringBootTest
@Transactional
class PostRepositoryTest {

    @Autowired PostRepository postRepository;

    @Test
    @Rollback(false)
    void save() {
        Post savedPost = postRepository.save(Post.create("test title 3", "test contents 3"));
        Post findPost = postRepository.getById(savedPost.getId());

        log.info("savedPost : {}", savedPost);
        log.info("findPost  : {}", findPost);

        assertThat(savedPost.getTitle()).isEqualTo(findPost.getTitle());
    }

}