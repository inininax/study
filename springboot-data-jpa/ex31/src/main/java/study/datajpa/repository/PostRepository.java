package study.datajpa.repository;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.repository.history.RevisionRepository;
import study.datajpa.domain.entity.Post;

public interface PostRepository extends JpaRepository<Post, Long>, RevisionRepository<Post, Long, Long> {
}
