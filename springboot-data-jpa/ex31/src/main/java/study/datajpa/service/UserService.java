package study.datajpa.service;

import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import study.datajpa.domain.entity.User;
import study.datajpa.repository.UserRepository;

import java.util.List;

@Service
@Transactional(readOnly = true)
@RequiredArgsConstructor
public class UserService {
    private final UserRepository repository;

    @Transactional
    public List<User> findAll() {
        return repository.findAll();
    }

    public List<User> findAllBySlave() {
        return repository.findAll();
    }
}
