package example.jwt.config;

import example.jwt.domain.dto.res.UserDto;
import lombok.extern.slf4j.Slf4j;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.data.domain.AuditorAware;
import org.springframework.data.jpa.repository.config.EnableJpaAuditing;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.context.SecurityContext;
import org.springframework.security.core.context.SecurityContextHolder;

import java.util.Optional;

/**
 * skip: @EnableJpaRepositories(basePackages = "example.jwt.repository", repositoryImplementationPostfix = "Impl")
 */
@Slf4j
@Configuration
@EnableJpaAuditing
public class JpaConfig {

    @Bean
    public AuditorAware<Long> auditorProvider() {
        return () -> {
            /*Authentication authentication = SecurityContextHolder.getContext().getAuthentication();
            log.debug("authentication                   : {}", authentication);
            log.debug("authentication.isAuthenticated() : {}", authentication == null ? "null" : authentication.isAuthenticated());
            log.debug("authentication.getDetails()      : {}", authentication == null ? "null" : authentication.getDetails());
            log.debug("authentication                   : {}", authentication == null ? "null" : authentication instanceof UserDto);*/

            return Optional.ofNullable(SecurityContextHolder.getContext())
                    .map(SecurityContext::getAuthentication)
                    .filter(Authentication::isAuthenticated)
                    .filter(authentication -> authentication.getDetails() instanceof UserDto)
                    .map(Authentication::getDetails)
                    .map(UserDto.class::cast)
                    .map(UserDto::getId)
                    .or(() -> Optional.of(0L));
        };
    }

}