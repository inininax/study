package study.datajpa;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.data.domain.AuditorAware;
import org.springframework.data.jpa.repository.config.EnableJpaAuditing;
import org.springframework.data.jpa.repository.config.EnableJpaRepositories;

import java.util.Optional;
import java.util.UUID;

/**
 * @EnableJpaRepositories(basePackages = "study.datajpa.repository")
 * - Application 하위에 있기 때문에 생략 가능
 * - Application 하위에 없을 경우 지정 필요
 */
@Configuration
@EnableJpaRepositories(basePackages = "study.datajpa.repository", repositoryImplementationPostfix = "Impl")
@EnableJpaAuditing
public class AppConfig {

    //실무에서는 spring security login 정보를 id로 활용
    @Bean
    public AuditorAware<String> auditorAware() {
        //spring security holder에서 정보를 가져와 출력
        return () -> Optional.of(UUID.randomUUID().toString());
    }

}
