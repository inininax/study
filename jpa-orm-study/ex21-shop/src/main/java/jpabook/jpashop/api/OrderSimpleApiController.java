package jpabook.jpashop.api;

import jpabook.jpashop.domain.Order;
import jpabook.jpashop.domain.OrderSearch;
import jpabook.jpashop.repository.order.simplequery.OrderSimpleQueryRepository;
import jpabook.jpashop.service.simplequery.OrderSimpleQueryService;
import jpabook.jpashop.service.simplequery.Result;
import lombok.RequiredArgsConstructor;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;

/**
 * API 개발 고급 - 지연 로딩과 조회 성능 최적화
 * 중요 [X to One]의 예제
 *
 * <p>
 * xToOne (ManyToOne, OneToOne) 관계 최적화
 * <p>
 * Order
 * Order -> Member
 * Order -> Delivery
 * <p>
 * 엔티티를 DTO로 변환하거나, DTO로 바로 조회하는 두가지 방법은 각각 장단점이 있다.
 * 둘중 상황에 따라서 더 나은 방법을 선택하면 된다.
 * 엔티티로 조회하면 리포지토리 재사용성도 좋고, 개발도 단순해진다.
 * 따라서 권장하는 방법은 다음과 같다.
 * <p>
 * 쿼리 방식 선택 권장 순서
 * 1. 우선 엔티티를 DTO로 변환하는 방법을 선택한다.
 * 2. 필요하면 페치 조인으로 성능을 최적화 한다. 대부분의 성능 이슈가 해결된다.
 * 3. 그래도 안되면 DTO로 직접 조회하는 방법을 사용한다.
 * 4. 최후의 방법은 JPA가 제공하는 네이티브 SQL이나 스프링 JDBC Template을 사용해서 SQL을 직접 사용한다.
 */
@RequiredArgsConstructor
@RestController
public class OrderSimpleApiController {

    private final OrderSimpleQueryService orderSimpleQueryService;
    //private final OrderRepository orderRepository;
    private final OrderSimpleQueryRepository orderSimpleQueryRepository;

    /**
     * V1. 엔티티 직접 노출
     * - Hibernate5Module 모듈 등록, LAZY=null 처리
     * - 양방향 관계 문제 발생 -> @JsonIgnore
     * <p>
     * 기본 동작 시 오류 발생
     * - order->member와 order->address는 fetch=LAZY(지연로딩)이다. 따라서 실제 엔티티가 대시 프록시로 존재한다.
     * - jackson 라이브러리는 기본적으로 이 프록시 객체를 json으로 어떻게 생성해야 하는지 모르기 때문에 예외가 발생한다.
     * - (프록시 라이브러리 ByteBuddy)
     * <p>
     * 해결법
     * - Hibernate5Module을 스프링 빈으로 등록한다.
     */
    @GetMapping("/api/v1/simple-orders")
    public List<Order> ordersV1() {
        // 01 order 내부의 무한 참조 에러 발생
        // List<Order> all = orderRepository.findAllByString(new OrderSearch());
        // return all;

        // 02 order와 양방향 관계를 가진 모든 부분에 @JsonIgnore를 추가
        // 03 fetch=LAZY 일 경우 실제 엔티티가 아닌 프록시 객체를 가져온다.
        //    jackson 라이브러리는 프록시 객체를 json으로 처리하기 못하기 때문에 오류가 발생한다.
        //    Hibernate5Module을 스프링 빈으로 등록하여 에러를 처리해 줄 수 있다.
        //    (프록시 라이브러리 ByteBuddy)
        /*
        List<Order> all = orderRepository.findAllByString(new OrderSearch());
        for (Order order : all) {
            order.getMember().getName(); // Lazy 강제 초기화
            order.getDelivery().getAddress(); // Lazy 강제 초기화
        }
        return all;
        */
        return orderSimpleQueryService.findAll_entity(new OrderSearch());
    }

    /**
     * V2. 엔티티를 조회하여 DTO로 변환 (fetch join 사용하지 않은 경우 예시)
     * - 단점: 지연로딩으로 쿼리 N번 호출
     * <p>
     * order 조회 1번 (order 조회 결과 수가 n이 된다.)
     * order->member 지연 로딩으로 조회 n번
     * order->delivery 지연 로딩으로 조회 n번
     * 총 1 + n + n 번 쿼리가 실행된다. 성능 문제 발생
     */
    @GetMapping("/api/v2/simple-orders")
    public Result ordersV2() {
        /*
        List<Order> orders = orderRepository.findAllByString(new OrderSearch());
        List<SimpleOrderDto> result = orders.stream()
                .map(order -> new SimpleOrderDto(order))
                .collect(Collectors.toList());
        return new Result(result);
        */

        /*
        return new Result(orderRepository.findAllByString(new OrderSearch()).stream()
                .map(SimpleOrderDto::new)
                .collect(toList()));

        */
        return orderSimpleQueryService.findAll_dto(new OrderSearch());
    }


    /**
     * V3. 엔티티를 조회해서 DTO 변환 (fetch join 사용한 경우 예시)
     * - fetch join으로 쿼리 1번 호출
     * <p>
     * JPQL의 fetch join을 통해 하나의 쿼리로 조회 가능
     * order->member
     */
    @GetMapping("/api/v3/simple-orders")
    public Result ordersV3() {
        /*
        List<Order> orders = orderRepository.findAllWithMemberDelivery();
        List<SimpleOrderDto> result = orders.stream()
                .map(order -> new SimpleOrderDto(order))
                .collect(Collectors.toList());
        return new Result(result);
        */

        /*
        return new Result(orderRepository.findAllWithMemberDelivery().stream()
                .map(SimpleOrderDto::new)
                .collect(toList()));
        */
        return orderSimpleQueryService.findAllWithMemberDelivery();
    }

    /**
     * V4. JPQL을 통해 DTO로 바로 조회
     * - 쿼리 1번 조회
     * - select 절에서 원하는 데이터만 선택해서 조회
     * <p>
     * 일반적인 SQL을 사용할 때 처럼 원하는 값을 선택해서 조회
     * new 명령어를 사용해서 JPQL의 결과를 DTO로 즉시 변환
     * SELECT 절에서 원하는 데이터를 직접 선택하므로 DB 애플리케이션 네트웍 용량 최적화(생각보다 미비)
     * 리포지토리 재사용성 떨어짐, API 스펙에 맞춘 코드가 리포지토리에 들어가는 단점
     */
    @GetMapping("/api/v4/simple-orders")
    public Result ordersV4() {
        return new Result(orderSimpleQueryRepository.findOrderDtos());
    }

}