# jpa orm study
## 강의 원문
- [김영한의 스프링 부트와 JPA 실무 완전 정복 로드맵](https://www.inflearn.com/roadmaps/149)

## Examples
- [ex01 hello jpa & 영속성 관리](./ex01-hello-jpa/README.md)
- [ex02 엔티티 매핑 & 연관관계 매핑](./ex02-model/README.md)
- [ex03 다양한 연관관계 매핑](./ex03-model/README.md)
- [ex04 다양한 연관관계 매핑](./ex04-model/README.md)
- [ex05 다양한 연관관계 매핑](./ex05-model/README.md)
- [ex06 고급 매핑](./ex06-model/README.md)
- [ex07 고급 매핑](./ex07-model/README.md)
- [ex08 프록시와 연관관계 관리 (Proxy, Fetch)](./ex08-proxy/README.md)
- [ex09 값 타입](./ex09-type/README.md)
- [ex10 값 타입](./ex10-type/README.md)
- [ex11 객체지향 쿼리 언어](./ex11-jpql/README.md)
- [ex12 JPA 활용 예제](./ex21-shop/README.md)

## Test Database
### Docker mariadb
- Driver: org.mariadb.jdbc.Driver
- Username: root
- Password: 1234
- URL: jdbc:mariadb://localhost:3306/ex01

```shell
docker run -p 127.0.0.1:3306:3306 --name test-mariadb -e MARIADB_ROOT_PASSWORD=1234 -d mariadb
docker start test-mariadb
docker exec -it some-mariadb bash
docker logs some-mariadb
```

### Example DML
```sql
create schema ex01;
use ex01;
create table Member
(
    id   bigint not null,
    name varchar(255),
    primary key (id)
);
```