# JPA 활용 예제
## 예제
- api package simpleorder -> order 순으로 작성

## 최적화
- OSIV ( Open Session In View ): Hibernate
- Open EntityManager In View: JPA
- 관례상 OSIV라고 칭함
```text
구동 오류 시 open-in-view true 설정 (실무에선 사용 안함)

spring:
  jpa:
    open-in-view: false # OSIV와 성능 최적화, off 시 transaction 조욜 전 모든 lazy 로딩을 사용해야 한다.
```