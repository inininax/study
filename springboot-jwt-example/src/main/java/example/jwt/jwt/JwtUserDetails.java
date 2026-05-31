package example.jwt.jwt;

import lombok.Getter;
import org.springframework.security.core.GrantedAuthority;
import org.springframework.security.core.authority.SimpleGrantedAuthority;
import org.springframework.security.core.userdetails.User;

import java.util.Collection;
import java.util.stream.Collectors;

@Getter
public class JwtUserDetails extends User {

    private Long id;

    public JwtUserDetails(String username, String password, Collection<? extends GrantedAuthority> authorities, Long id) {
        super(username, password, authorities);
        this.id = id;
    }

    public static JwtUserDetails from(example.jwt.domain.entity.User user) {
        return new JwtUserDetails(
                user.getUsername(),
                user.getPassword(),
                user.getUserAuthorities().stream()
                        .map(userAuthority -> new SimpleGrantedAuthority(userAuthority.getAuthority().getName()))
                        .collect(Collectors.toList()),
                user.getId()
        );
    }

}
