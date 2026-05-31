package example.jwt.service;

import example.jwt.domain.dto.res.UserDto;
import example.jwt.jwt.JwtUserDetails;
import org.springframework.context.annotation.Lazy;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.authentication.dao.DaoAuthenticationProvider;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.security.core.userdetails.UserDetailsService;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Component;

/**
 * org.springframework.security.authentication.dao.AbstractUserDetailsAuthenticationProvider
 * org.springframework.security.authentication.dao.DaoAuthenticationProvider
 */
@Component
public class CustomAuthenticationProvider extends DaoAuthenticationProvider {

    public CustomAuthenticationProvider(@Lazy UserDetailsService userDetailsService, @Lazy PasswordEncoder passwordEncoder) {
        this.setUserDetailsService(userDetailsService);
        this.setPasswordEncoder(passwordEncoder);
    }

    @Override
    protected Authentication createSuccessAuthentication(Object principal, Authentication authentication, UserDetails userDetails) {
        ((UsernamePasswordAuthenticationToken) authentication).setDetails(UserDto.from(((JwtUserDetails) userDetails).getId()));
        return super.createSuccessAuthentication(principal, authentication, userDetails);
    }

}
