package study.datajpa.config;

import com.querydsl.jpa.impl.JPAQueryFactory;
import lombok.extern.slf4j.Slf4j;
import org.springframework.boot.autoconfigure.orm.jpa.HibernateProperties;
import org.springframework.boot.autoconfigure.orm.jpa.HibernateSettings;
import org.springframework.boot.autoconfigure.orm.jpa.JpaProperties;
import org.springframework.boot.orm.jpa.EntityManagerFactoryBuilder;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.data.domain.AuditorAware;
import org.springframework.orm.jpa.JpaTransactionManager;
import org.springframework.orm.jpa.LocalContainerEntityManagerFactoryBean;
import org.springframework.transaction.PlatformTransactionManager;
import study.datajpa.domain.entity.User;

import javax.persistence.EntityManager;
import javax.persistence.EntityManagerFactory;
import javax.sql.DataSource;
import java.util.Map;
import java.util.Objects;
import java.util.Optional;

@Slf4j
@Configuration
public class JpaConfig {
    @Bean
    public AuditorAware<User> auditorAware() {
        //TODO auditorAware
        return () -> Optional.of(User.dummy());
    }

    /**
     * @ConfigurationProperties(prefix = "spring.jpa") JpaProperties jpaProperties
     * @ConfigurationProperties("spring.jpa.hibernate") HibernateProperties hibernateProperties
     */
    @Bean
    public LocalContainerEntityManagerFactoryBean entityManagerFactory(JpaProperties jpaProperties,
                                                                       HibernateProperties hibernateProperties,
                                                                       EntityManagerFactoryBuilder builder,
                                                                       DataSource dataSource) {
        Map<String, Object> properties = hibernateProperties.determineHibernateProperties(jpaProperties.getProperties(), new HibernateSettings());
        return builder.dataSource(dataSource)
                .properties(properties)
                .packages("study.datajpa.domain.entity")
                .persistenceUnit("entityManager")
                .build();
    }

    @Bean
    public JPAQueryFactory queryFactory(EntityManager entityManager) {
        return new JPAQueryFactory(entityManager);
    }

    @Bean
    public PlatformTransactionManager transactionManager(EntityManagerFactory entityManagerFactory) {
        return new JpaTransactionManager(Objects.requireNonNull(entityManagerFactory));
    }
}
