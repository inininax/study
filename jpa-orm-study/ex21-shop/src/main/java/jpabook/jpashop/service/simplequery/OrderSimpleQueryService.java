package jpabook.jpashop.service.simplequery;

import jpabook.jpashop.domain.Order;
import jpabook.jpashop.domain.OrderSearch;
import jpabook.jpashop.repository.OrderRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;

import static java.util.stream.Collectors.toList;

/**
 * open-in-view: false 로 인해
 * 엔티티 그래프 탐색 시 오류 방지를 위해
 * transaction 관리를 위한 이동
 */
@RequiredArgsConstructor
@Transactional(readOnly = true)
@Service
public class OrderSimpleQueryService {
    private final OrderRepository orderRepository;

    public List<Order> findAll_entity(OrderSearch orderSearch) {
        List<Order> all = orderRepository.findAllByString(orderSearch);
        for (Order order : all) {
            order.getMember().getName(); // Lazy 강제 초기화
            order.getDelivery().getAddress(); // Lazy 강제 초기화

            // open-in-view: false # OSIV와 성능 최적화, off 시 transaction 조욜 전 모든 lazy 로딩을 사용해야 한다.
            order.getOrderItems().forEach(orderItem -> orderItem.getItem());
        }
        return all;
    }

    public Result findAll_dto(OrderSearch orderSearch) {
        return new Result(orderRepository.findAllByString(new OrderSearch()).stream()
                .map(SimpleOrderDto::new)
                .collect(toList()));
    }

    public Result findAllWithMemberDelivery() {
        return new Result(orderRepository.findAllWithMemberDelivery().stream()
                .map(SimpleOrderDto::new)
                .collect(toList()));
    }
}