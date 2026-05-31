package jpabook.jpashop.repository.order.query;

import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Repository;

import javax.persistence.EntityManager;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

@RequiredArgsConstructor
@Repository
public class OrderQueryRepository {

    private final EntityManager em;

    /**
     * 컬렉션은 별도로 조회
     * Query: 루트 1번, 컬렉션 N 번
     * 단건 조회에서 많이 사용하는 방식
     * <p>
     * 1 + N(컬렉션) 문제가 존재함
     */
    public List<OrderQueryDto> findOrderQueryDtos(int offset, int limit) {
        // 주문 조회 (to one 코드를 모두 한번에 조회)
        List<OrderQueryDto> result = findOrders(offset, limit);

        // 루프를 돌면서 컬렉션 추가( 추가 쿼리 실행 )
        result.forEach(o -> {
            List<OrderItemQueryDto> orderItems = findOrderItmes(o.getOrderId());
            o.setOrderItems(orderItems);
        });

        return result;
    }

    /**
     * 최적화
     * Query: 루트 1번, 컬렉션 1번
     * 데이터를 한꺼번에 처리할 때 많이 사용하는 방식
     */
    public List<OrderQueryDto> findAllByDto_optimization(int offset, int limit) {
        // 루트 조회(toOne 코드를 모두 한번에 조회)
        List<OrderQueryDto> result = findOrders(offset, limit);

        // orderItem 컬렉션을 MAP 한방에 조회
        Map<Long, List<OrderItemQueryDto>> orderItemMap = findOrderItemMap(toOrderIds(result));

        // 루프를 돌면서 컬렉션 추가(추가 쿼리 실행X)
        result.forEach(o -> o.setOrderItems(orderItemMap.get(o.getOrderId())));

        return result;
    }

    public List<OrderFlatDto> findAllByDto_flat() {
        return em.createQuery(
                "select new jpabook.jpashop.repository.order.query.OrderFlatDto( o.id, m.name, o.orderDate, o.status, d.address, i.name, oi.orderPrice, oi.count ) " +
                        " from Order o " +
                        " join o.member m " +
                        " join o.delivery d " +
                        " join o.orderItems oi " +
                        " join oi.item i ", OrderFlatDto.class)
                .getResultList();
    }

    private List<OrderQueryDto> findOrders(int offset, int limit) {
        return em.createQuery(
                "select new jpabook.jpashop.repository.order.query.OrderQueryDto( o.id, m.name, o.orderDate, o.status, d.address ) " +
                        " from Order o " +
                        " join o.member m " + // to one
                        " join o.delivery d ", OrderQueryDto.class) // to one
                .setFirstResult(offset)
                .setMaxResults(limit)
                .getResultList();
    }

    private List<OrderItemQueryDto> findOrderItmes(Long orderId) {
        return em.createQuery(
                "select new jpabook.jpashop.repository.order.query.OrderItemQueryDto( oi.order.id, i.name, oi.orderPrice, oi.count ) " +
                        " from OrderItem oi " +
                        " join oi.item i" +
                        " where oi.order.id = :orderId ", OrderItemQueryDto.class)
                .setParameter("orderId", orderId)
                .getResultList();
    }

    private List<Long> toOrderIds(List<OrderQueryDto> result) {
        return result.stream()
                .map(OrderQueryDto::getOrderId)
                .collect(Collectors.toList());
    }

    private Map<Long, List<OrderItemQueryDto>> findOrderItemMap(List<Long> orderIds) {
        List<OrderItemQueryDto> orderItems = em.createQuery(
                "select new jpabook.jpashop.repository.order.query.OrderItemQueryDto( oi.order.id, i.name, oi.orderPrice, oi.count ) " +
                        " from OrderItem oi " +
                        " join oi.item i" +
                        " where oi.order.id in :orderIds ", OrderItemQueryDto.class)
                .setParameter("orderIds", orderIds)
                .getResultList();

        return orderItems.stream()
                .collect(Collectors.groupingBy(OrderItemQueryDto::getOrderId));
    }

}