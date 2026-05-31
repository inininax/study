# springboot data jpa study
## 강의 원문
- [김영한의 스프링 부트와 JPA 실무 완전 정복 로드맵](https://www.inflearn.com/roadmaps/149)

## Examples
- [JPA Examples](https://github.com/barrier-free/study-jpa)
- [ex22 - JPA Example](./ex22-shop/README.md)
- [ex23 - DATA JPA Example](./ex23-datajpa/README.md)
- [ex24 - QueryDSL Example](./ex24-querydsl/README.md)

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