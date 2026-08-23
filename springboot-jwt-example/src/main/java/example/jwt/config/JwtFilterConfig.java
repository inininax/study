package example.jwt.config;

import example.jwt.jwt.JwtFilter;
import example.jwt.jwt.TokenProvider;
import org.springframework.boot.web.servlet.FilterRegistrationBean;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

/**
 * JwtFilter 빈 정의를 SecurityConfig 밖으로 분리한 설정.
 * SecurityConfig가 JwtSecurityConfig를 주입받고, 그 JwtSecurityConfig가 JwtFilter를
 * 필요로 하므로 jwtFilter @Bean이 SecurityConfig 안에 있으면 순환 참조가 발생한다.
 */
@Configuration
public class JwtFilterConfig {

    @Bean
    public JwtFilter jwtFilter(TokenProvider tokenProvider) {
        return new JwtFilter(tokenProvider);
    }

    // JwtFilter 빈의 서블릿 컨테이너 전역 자동 등록을 막아
    // JwtSecurityConfig 를 통한 시큐리티 체인 내 단일 등록만 유지한다.
    @Bean
    public FilterRegistrationBean<JwtFilter> jwtFilterRegistrationBean(JwtFilter jwtFilter) {
        FilterRegistrationBean<JwtFilter> registration = new FilterRegistrationBean<>(jwtFilter);
        registration.setEnabled(false);
        return registration;
    }
}
