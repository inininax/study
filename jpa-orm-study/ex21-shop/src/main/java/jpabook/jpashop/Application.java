package jpabook.jpashop;

import com.fasterxml.jackson.datatype.hibernate5.Hibernate5Module;
import lombok.extern.slf4j.Slf4j;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.annotation.Bean;

@Slf4j
@SpringBootApplication
public class Application {

    public static void main(String[] args) {
        SpringApplication.run(Application.class, args);
    }

    // 실무에서는 entity를 직접 노출하지 않기 때문에 사용하지 않음, 에러 처리를 위한 예시로 사용
    // implementation 'com.fasterxml.jackson.datatype:jackson-datatype-hibernate5'
    @Bean
    public Hibernate5Module hibernate5Module() {
        final Hibernate5Module hibernate5Module = new Hibernate5Module();

        // *이렇게 사용하지 말 것 예시로만 참고*
        // LAZY 로딩을 무시하고 json 생성 시 강제로 Lazy로딩을 실행 시켜버림
        //hibernate5Module.configure(Hibernate5Module.Feature.FORCE_LAZY_LOADING, true);

        return hibernate5Module;
    }

}
