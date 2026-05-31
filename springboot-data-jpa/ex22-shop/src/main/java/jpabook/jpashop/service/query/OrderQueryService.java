package jpabook.jpashop.service.query;

import jpabook.jpashop.domain.entity.Order;
import jpabook.jpashop.domain.entity.OrderItem;
import jpabook.jpashop.domain.dto.OrderSearch;
import jpabook.jpashop.repository.OrderRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;
import java.util.stream.Collectors;

/**
 * open-in-view: false 로 인해
 * 엔티티 그래프 탐색 시 오류 방지를 위해
 * transaction 관리를 위한 이동
 */
@RequiredArgsConstructor
@Transactional(readOnly = true)
@Service
public class OrderQueryService {
    private final OrderRepository orderRepository;

    public List<Order> findAll_entity(OrderSearch orderSearch) {
        List<Order> all = orderRepository.findAllByString(orderSearch);

        // open-in-view: true 일 경우 사용 가능하지만 커넥션을 너무 긴 시간 동안 물고 있어 장애의 원인이 된다.
        // fetch join으로 변경하던지 서비스로 코드 이동
        for (Order order : all) {
            order.getMember().getName(); // Lazy 강제 초기화 , member jsonIgnore 처리되어 있음
            order.getDelivery().getAddress(); // Lazy 강제 초기화 , member jsonIgnore 처리되어 있음
            List<OrderItem> orderItems = order.getOrderItems();
            orderItems.stream().forEach(orderItem -> orderItem.getItem().getName()); // Lazy 강제 초기화
        }

        return all;
    }

    public List<OrderDto> findAll_dto(OrderSearch orderSearch) {
        return orderRepository.findAllByString(orderSearch).stream()
                .map(OrderDto::new)
                .collect(Collectors.toList());
    }

    public List<OrderDto> findAllWithItem() {
        return orderRepository.findAllWithItem().stream()
                .map(OrderDto::new)
                .collect(Collectors.toList());
    }

    public List<OrderDto> findAllWithMemberDelivery(int offset, int limit) {
        List<Order> orders = orderRepository.findAllWithMemberDelivery(offset, limit);
        List<OrderDto> result = orders.stream()
                .map(order -> new OrderDto(order))
                .collect(Collectors.toList());
        return result;
    }

}