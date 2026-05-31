package jpabook.jpashop.api;

import jpabook.jpashop.domain.entity.Order;
import jpabook.jpashop.domain.dto.OrderSearch;
import jpabook.jpashop.repository.OrderRepository;
import jpabook.jpashop.repository.order.query.OrderFlatDto;
import jpabook.jpashop.repository.order.query.OrderItemQueryDto;
import jpabook.jpashop.repository.order.query.OrderQueryDto;
import jpabook.jpashop.repository.order.query.OrderQueryRepository;
import jpabook.jpashop.service.query.OrderDto;
import jpabook.jpashop.service.query.OrderQueryService;
import lombok.RequiredArgsConstructor;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;

import static java.util.stream.Collectors.*;

/**
 * API 개발 고급 - 컬렉션 조회 최적화
 * 중요 [X to Many]의 예제
 *
 * <p>
 * 앞의 예제에서는 toOne(OneToOne, ManyToOne) 관계만 있었다. 이번에는 컬렉션인 일대다 관계
 * (OneToMany)를 조회하고, 최적화하는 방법을 알아보자.
 * <p>
 * V1. 엔티티 직접 노출
 * - 엔티티가 변하면 API 스펙이 변한다.
 * - 트랜잭션 안에서 지연 로딩 필요
 * - 양방향 연관관계 문제
 * <p>
 * V2. 엔티티를 조회해서 DTO로 변환(fetch join 사용X)
 * - 트랜잭션 안에서 지연 로딩 필요
 * <p>
 * V3. 엔티티를 조회해서 DTO로 변환(fetch join 사용O)
 * - 페이징 시에는 N 부분을 포기해야함(대신에 batch fetch size? 옵션 주면 N -> 1 쿼리로 변경 가능)
 * <p>
 * V4.JPA에서 DTO로 바로 조회, 컬렉션 N 조회 (1+NQuery)
 * - 페이징 가능
 * <p>
 * V5.JPA에서 DTO로 바로 조회, 컬렉션 1 조회 최적화 버전 (1+1Query)
 * - 페이징 가능
 * <p>
 * V6. JPA에서 DTO로 바로 조회, 플랫 데이터(1Query) (1 Query)
 * - 페이징 불가능...
 */
@RequiredArgsConstructor
@RestController
public class OrderApiController {
    private final OrderQueryService orderQueryService;
    private final OrderRepository orderRepository;
    private final OrderQueryRepository orderQueryRepository;

    /**
     * V1. 엔티티 직접 노출
     * - Hibernate5Module 모듈 등록으로 인해 LAZY=null 처리
     * - 양방향 관계 문제 발생 -> @JsonIgnore
     * <p>
     * orderItem , item 관계를 직접 초기화하면 Hibernate5Module 설정에 의해 엔티티를 JSON으로 생성한다.
     * 양방향 연관관계면 무한 루프에 걸리지 않게 한곳에 @JsonIgnore 를 추가해야 한다.
     * 엔티티를 직접 노출하므로 좋은 방법은 아니다.
     */
    @GetMapping("/api/v1/orders")
    public List<Order> ordersV1() {
        // open-in-view: true 일 경우 사용 가능하지만 커넥션을 너무 긴 시간 동안 물고 있어 장애의 원인이 된다.
        // fetch join으로 변경하던지 서비스로 코드 이동
        /*
        List<Order> all = orderRepository.findAllByString(new OrderSearch());
        for (Order order : all) {
            order.getMember().getName(); // Lazy 강제 초기화 , member jsonIgnore 처리되어 있음
            order.getDelivery().getAddress(); // Lazy 강제 초기화 , member jsonIgnore 처리되어 있음
            List<OrderItem> orderItems = order.getOrderItems();
            orderItems.stream().forEach(orderItem -> orderItem.getItem().getName()); // Lazy 강제 초기화
        }
        return all;
        */
        return orderQueryService.findAll_entity(new OrderSearch());
    }

    /**
     * V2. 엔티티를 DTO로 변환
     * - 지연 로딩으로 너무 많은 SQL 실행
     * <p>
     * 참고: 지연 로딩은 영속성 컨텍스트에 있으면 영속성 컨텍스트에 있는 엔티티를 사용하고 없으면 SQL을 실행한다.
     * 따라서 같은 영속성 컨텍스트에서 이미 로딩한 회원 엔티티를 추가로 조회하면 SQL을 실행하지 않는다.
     */
    @GetMapping("/api/v2/orders")
    public List<OrderDto> ordersV2() {
        /*
        return orderRepository.findAllByString(new OrderSearch()).stream()
                .map(OrderDto::new)
                .collect(toList());
        */
        return orderQueryService.findAll_dto(new OrderSearch());
    }

    /**
     * V3. 엔티티를 DTO로 변환 - 페치 조인 최적화
     * <p>
     * <p>
     * 페치 조인으로 SQL이 1번만 실행됨
     * <p>
     * distinct를 사용한 이유는 1대다 조인이 있으므로 데이터베이스 row가 증가한다.
     * 그 결과 같은 order 엔티티의 조회 수도 증가하게 된다.
     * JPA의 distinct는 SQL에 distinct를 추가하고, 더해서 같은 엔티티가 조회되면, 애플리케이션에서 중복을 걸러준다.
     * 이 예제에서는 order가 컬렉션 페치 조인 때문에 중복 조회 되는 것을 막아준다.
     * <p>
     * 참고: 컬렉션 페치 조인을 사용하면 페이징이 불가능하다.
     * 하이버네이트는 경고 로그를 남기면서 모든 데이터를 DB에서 읽어오고, 메모리에서 페이징 해버린다(매우 위험하다).
     * 자세한 내용은 자바 ORM 표준 JPA 프로그래밍의 페치 조인 부분을 참고하자.
     * <p>
     * 참고: 컬렉션 페치 조인은 1개만 사용할 수 있다.
     * 컬렉션 둘 이상에 페치 조인을 사용하면 안된다. 데이터가 부정합하게 조회될 수 있다.
     * 자세한 내용은 자바 ORM 표준 JPA 프로그래밍을 참고하자.
     */
    @GetMapping("/api/v3/orders")
    public List<OrderDto> ordersV3() {
        /*
        return orderRepository.findAllWithItem().stream()
                .map(OrderDto::new)
                .collect(toList());
        */
        return orderQueryService.findAllWithItem();
    }

    /**
     * V3.1. 엔티티를 DTO로 변환 - 페이징과 한계 돌파
     * <p>
     * 컬렉션을 페치 조인하면 페이징이 불가능하다.
     * <p>
     * 1. 먼저 ToOne(OneToOne, ManyToOne) 관계를 모두 페치조인 한다.
     * ToOne 관계는 row수를 증가시키지 않으므로 페이징 쿼리에 영향을 주지 않는다.
     * <p>
     * 2. 컬렉션은 지연 로딩으로 조회한다.
     * <p>
     * 3. 지연 로딩 성능 최적화를 위해 hibernate.default_batch_fetch_size , @BatchSize 를 적용한다.
     * - hibernate.default_batch_fetch_size: 글로벌 설정
     * - @BatchSize: 개별 최적화
     * - 이 옵션을 사용하면 컬렉션이나, 프록시 객체를 한꺼번에 설정한 size 만큼 IN 쿼리로 조회한다.
     */
    @GetMapping("/api/v3.1/orders")
    public List<OrderDto> ordersV3_page(@RequestParam(name = "offset", defaultValue = "0") int offset,
                                        @RequestParam(name = "limit", defaultValue = "100") int limit) {
        /*
        List<Order> orders = orderRepository.findAllWithMemberDelivery(offset, limit);
        List<OrderDto> result = orders.stream()
                .map(order -> new OrderDto(order))
                .collect(toList());
        return result;
        */
        return orderQueryService.findAllWithMemberDelivery(offset, limit);
    }

    /**
     * V4. JPA에서 DTO 직접 조회
     * <p>
     * Query: 루트 1번, 컬렉션 N 번 실행
     * ToOne(N:1, 1:1) 관계들을 먼저 조회하고, ToMany(1:N) 관계는 각각 별도로 처리한다.
     * - 이런 방식을 선택한 이유는 다음과 같다.
     * - ToOne 관계는 조인해도 데이터 row 수가 증가하지 않는다.
     * - ToMany(1:N) 관계는 조인하면 row 수가 증가한다.
     * row 수가 증가하지 않는 ToOne 관계는 조인으로 최적화 하기 쉬우므로 한번에 조회하고,
     * ToMany 관계는 최적화 하기 어려우므로 findOrderItems() 같은 별도의 메서드로 조회한다.
     */
    @GetMapping("/api/v4/orders")
    public List<OrderQueryDto> ordersV4(@RequestParam(name = "offset", defaultValue = "0") int offset,
                                        @RequestParam(name = "limit", defaultValue = "100") int limit) {
        return orderQueryRepository.findOrderQueryDtos(offset, limit);
    }

    /**
     * V5. JPA에서 DTO로 직접 조회 - 컬렉션 조회 최적화
     */
    @GetMapping("/api/v5/orders")
    public List<OrderQueryDto> ordersV5(@RequestParam(name = "offset", defaultValue = "0") int offset,
                                        @RequestParam(name = "limit", defaultValue = "100") int limit) {
        return orderQueryRepository.findAllByDto_optimization(offset, limit);
    }

    /**
     * V6. JPA에서 DTO로 직접 조회 - 플랫 데이터 최적화
     * <p>
     * 단점
     * - 쿼리는 한번이지만 조인으로 인해 DB에서 애플리케이션에 전달하는 데이터에 중복 데이터가 추가되므로 상황에 따라 V5 보다 더 느릴 수 도 있다.
     * - 애플리케이션에서 추가 작업이 크다.
     * - 페이징 불가능
     */
    @GetMapping("/api/v6/orders")
    public List<OrderQueryDto> ordersV6() {
        List<OrderFlatDto> flats = orderQueryRepository.findAllByDto_flat();

        return flats.stream()
                .collect(
                        groupingBy(
                                orderFlatDto -> new OrderQueryDto(orderFlatDto.getOrderId(), orderFlatDto.getName(), orderFlatDto.getOrderDate(), orderFlatDto.getOrderStatus(), orderFlatDto.getAddress()),
                                mapping(
                                        orderFlatDto -> new OrderItemQueryDto(orderFlatDto.getOrderId(), orderFlatDto.getItemName(), orderFlatDto.getOrderPrice(), orderFlatDto.getCount()),
                                        toList()
                                )
                        )
                )
                .entrySet().stream()
                .map(e -> new OrderQueryDto(
                        e.getKey().getOrderId(),
                        e.getKey().getName(),
                        e.getKey().getOrderDate(),
                        e.getKey().getOrderStatus(),
                        e.getKey().getAddress(),
                        e.getValue()))
                .collect(toList());
    }


}