package example.jwt.service;

import example.jwt.domain.entity.User;
import example.jwt.jwt.JwtUserDetails;
import example.jwt.repository.UserRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.security.access.AccessDeniedException;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.security.core.userdetails.UserDetailsService;
import org.springframework.security.core.userdetails.UsernameNotFoundException;
import org.springframework.stereotype.Component;
import org.springframework.transaction.annotation.Transactional;

@Component("userDetailsService")
@RequiredArgsConstructor
public class CustomUserDetailService implements UserDetailsService {

    private final UserRepository userRepository;

    @Override
    @Transactional
    public UserDetails loadUserByUsername(String username) throws UsernameNotFoundException {
        return userRepository.findWithEntityGraphByUsername(username)
                .map(this::createUser)
                .orElseThrow(() -> new UsernameNotFoundException(username + " not found"));
    }

    private UserDetails createUser(User user) {
        if (!user.isActivated()) {
            throw new AccessDeniedException(user.getUsername() + " deactivated");
        }
        return JwtUserDetails.from(user);
    }

}
