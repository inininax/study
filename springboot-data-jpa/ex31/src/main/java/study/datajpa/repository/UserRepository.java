package study.datajpa.repository;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.repository.history.RevisionRepository;
import study.datajpa.domain.entity.User;

public interface UserRepository extends JpaRepository<User, Long>, UserRepositoryCustom, RevisionRepository<User, Long, Long> {
}