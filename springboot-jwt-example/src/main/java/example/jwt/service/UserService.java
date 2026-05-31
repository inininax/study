package example.jwt.service;

import example.jwt.domain.dto.req.SignupDto;
import example.jwt.domain.dto.res.UserDto;
import example.jwt.domain.entity.Authority;
import example.jwt.domain.entity.User;
import example.jwt.domain.entity.UserAuthority;
import example.jwt.repository.AuthorityRepository;
import example.jwt.repository.UserAuthorityRepository;
import example.jwt.repository.UserRepository;
import example.jwt.util.SecurityUtil;
import lombok.RequiredArgsConstructor;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import javax.persistence.EntityNotFoundException;

@Service
@RequiredArgsConstructor
@Transactional
public class UserService {

    private final PasswordEncoder passwordEncoder;
    private final AuthorityRepository authorityRepository;
    private final UserRepository userRepository;
    private final UserAuthorityRepository userAuthorityRepository;

    public UserDto signup(SignupDto signupDto) {
        if (userRepository.findWithEntityGraphByUsername(signupDto.getUsername()).isPresent()) {
            throw new RuntimeException("이미 가입되어 있는 유저입니다.");
        }

        Authority authority = authorityRepository.findByName("ROLE_USER").orElseThrow(EntityNotFoundException::new);

        User user = User.create(signupDto.getUsername(), passwordEncoder.encode(signupDto.getPassword()), signupDto.getName(), true);
        userRepository.save(user);

        UserAuthority userAuthority = UserAuthority.create(user, authority, true);
        userAuthorityRepository.save(userAuthority);

        return UserDto.from(user);
    }

    @Transactional(readOnly = true)
    public UserDto getUserWithAuthorities(String username) {
        return UserDto.from(userRepository.findWithEntityGraphByUsername(username)
                .orElseThrow(EntityNotFoundException::new));
    }

    @Transactional(readOnly = true)
    public UserDto getMyUserWithAuthorities() {
        return UserDto.from(SecurityUtil.getCurrentUsername()
                .flatMap(userRepository::findWithEntityGraphByUsername)
                .orElseThrow(EntityNotFoundException::new));
    }

}