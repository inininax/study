package example.jwt;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.context.ActiveProfiles;
import org.springframework.test.context.TestPropertySource;
import org.springframework.transaction.annotation.Transactional;

import javax.sql.DataSource;
import java.sql.Connection;

import static org.assertj.core.api.Assertions.assertThat;

/**
 * 로컬 MariaDB 없이 동작하는 최소 스모크 테스트.
 * localdb 프로필(MariaDB) 대신 H2 인메모리로 컨텍스트 기동을 검증한다.
 */
@SpringBootTest
@ActiveProfiles({"localjpa", "localjwt", "common"})
@TestPropertySource(properties = {
        "spring.datasource.driver-class-name=org.h2.Driver",
        "spring.datasource.url=jdbc:h2:mem:jwt-smoke;MODE=MariaDB;NON_KEYWORDS=USER;DB_CLOSE_DELAY=-1",
        "spring.datasource.username=sa",
        "spring.datasource.password=",
        "spring.jpa.hibernate.ddl-auto=create-drop",
        "decorator.datasource.p6spy.enable-logging=false"
})
@Transactional
class JwtExampleApplicationTests {

    @Autowired
    DataSource dataSource;

    @Test
    void contextLoads() {
        assertThat(dataSource).isNotNull();
    }

    @Test
    void datasourceIsUsable() throws Exception {
        try (Connection conn = dataSource.getConnection()) {
            assertThat(conn.isValid(1)).isTrue();
        }
    }
}
