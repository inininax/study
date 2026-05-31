package example.jwt.service;

import example.jwt.domain.dto.req.LoginDto;
import example.jwt.domain.dto.res.TokenDto;
import example.jwt.jwt.TokenProvider;
import lombok.RequiredArgsConstructor;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.config.annotation.authentication.builders.AuthenticationManagerBuilder;
import org.springframework.security.core.Authentication;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

@Service
@RequiredArgsConstructor
@Transactional
public class AuthService {

    private final AuthenticationManagerBuilder authenticationManagerBuilder;
    private final TokenProvider tokenProvider;

    public TokenDto authorize(LoginDto loginDto) {
        UsernamePasswordAuthenticationToken authenticationToken = new UsernamePasswordAuthenticationToken(loginDto.getUsername(), loginDto.getPassword());

        // CustomUserDetailService.loadUserByUsername
        // SecurityContextHolder.getContext().setAuthentication(authResult);
        Authentication authentication = authenticationManagerBuilder.getObject().authenticate(authenticationToken);

        // Create JWT
        return TokenDto.from(tokenProvider.createToken(authentication));
    }

}
