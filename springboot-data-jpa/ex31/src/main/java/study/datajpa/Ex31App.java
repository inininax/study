package study.datajpa;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.cloud.openfeign.EnableFeignClients;
import org.springframework.data.envers.repository.config.EnableEnversRepositories;
import org.springframework.data.jpa.repository.config.EnableJpaAuditing;

@SpringBootApplication
@EnableEnversRepositories
@EnableJpaAuditing
@EnableFeignClients
public class Ex31App {
    public static void main(String[] args) {
        SpringApplication.run(Ex31App.class, args);
    }
}
