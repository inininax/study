package study.jpa.config;

import org.hibernate.boot.model.naming.Identifier;
import org.hibernate.boot.model.naming.PhysicalNamingStrategy;
import org.hibernate.engine.jdbc.env.spi.JdbcEnvironment;

/**
 * 기존 hibernate.ejb.naming_strategy(ImprovedNamingStrategy, deprecated)와 동일하게
 * 카멜케이스를 snake_case 컬럼/테이블명으로 변환하는 물리 네이밍 전략.
 *
 * Hibernate 5.4 에는 Spring Boot 의 CamelCaseToUnderscoresNamingStrategy(hibernate 5.6+)가
 * 없어서 ImprovedNamingStrategy 동작을 그대로 재현했다.
 */
public class SnakeCasePhysicalNamingStrategy implements PhysicalNamingStrategy {

    @Override
    public Identifier toPhysicalCatalogName(Identifier name, JdbcEnvironment context) {
        return toSnake(name);
    }

    @Override
    public Identifier toPhysicalSchemaName(Identifier name, JdbcEnvironment context) {
        return toSnake(name);
    }

    @Override
    public Identifier toPhysicalTableName(Identifier name, JdbcEnvironment context) {
        return toSnake(name);
    }

    @Override
    public Identifier toPhysicalSequenceName(Identifier name, JdbcEnvironment context) {
        return toSnake(name);
    }

    @Override
    public Identifier toPhysicalColumnName(Identifier name, JdbcEnvironment context) {
        return toSnake(name);
    }

    private Identifier toSnake(Identifier name) {
        if (name == null) {
            return null;
        }
        String snake = name.getText().replaceAll("([a-z\\d])([A-Z])", "$1_$2").toLowerCase();
        return Identifier.toIdentifier(snake, name.isQuoted());
    }
}
