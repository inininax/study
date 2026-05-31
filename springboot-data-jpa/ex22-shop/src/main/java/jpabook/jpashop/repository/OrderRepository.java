package jpabook.jpashop.repository;

import jpabook.jpashop.domain.entity.Member;
import jpabook.jpashop.domain.entity.Order;
import jpabook.jpashop.domain.dto.OrderSearch;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Repository;

import javax.persistence.EntityManager;
import javax.persistence.TypedQuery;
import javax.persistence.criteria.*;
import java.util.ArrayList;
import java.util.List;

@RequiredArgsConstructor
@Repository
public class OrderRepository {
    private final EntityManager em;

    public void save(Order order) {
        em.persist(order);
    }

    public Order findOne(Long id) {
        return em.find(Order.class, id);
    }

    public List<Order> findAllByString(OrderSearch orderSearch) {
        // jpql
        String jpql = "select o from Order o join o.member m";
        boolean isFirstCondition = true;

        // 주문 상태 검색
        if (orderSearch.getOrderStatus() != null) {
            if (isFirstCondition) {
                jpql += " where";
                isFirstCondition = false;
            } else {
                jpql += " and";
            }
            jpql += " o.status = :status";
        }
        // 회원 이름 검색
        if (orderSearch.getMemberName() != null && !"".equals(orderSearch.getMemberName())) {
            if (isFirstCondition) {
                jpql += " where";
                isFirstCondition = false;
            } else {
                jpql += " and";
            }
            jpql += " m.name = :name";
        }
        TypedQuery<Order> query = em.createQuery(jpql, Order.class).setMaxResults(1000);
        if (orderSearch.getOrderStatus() != null) {
            query = query.setParameter("status", orderSearch.getOrderStatus());
        }
        if (orderSearch.getMemberName() != null && !"".equals(orderSearch.getMemberName())) {
            query = query.setParameter("name", orderSearch.getMemberName());
        }
        return query.getResultList();
    }

    public List<Order> findAllByCriteria(OrderSearch orderSearch) {
        CriteriaBuilder cb = em.getCriteriaBuilder();
        CriteriaQuery<Order> cq = cb.createQuery(Order.class);
        Root<Order> o = cq.from(Order.class);
        Join<Order, Member> m = o.join("member", JoinType.INNER);
        List<Predicate> criteria = new ArrayList<>();
        // 주만 상태 검색
        if (orderSearch.getOrderStatus() != null) {
            Predicate status = cb.equal(o.get("status"), orderSearch.getOrderStatus());
            criteria.add(status);
        }
        // 회원 이름 검색
        if (orderSearch.getMemberName() != null && !"".equals(orderSearch.getMemberName())) {
            Predicate name = cb.like(m.<String>get("name"), "%" + orderSearch.getMemberName() + "%");
            criteria.add(name);
        }
        cq.where(cb.and(criteria.toArray(new Predicate[criteria.size()])));
        TypedQuery<Order> query = em.createQuery(cq).setMaxResults(1000); // 최대 1000건
        return query.getResultList();
    }

    /*public List<Order> findAll(OrderSearch orderSearch) {
        return null;
    }

    public List<Order> findAll() {
        return null;
    }*/

    /**
     * simple-orders 예시 (x to one)
     * <p>
     * X to One 일 경우는 distinct 사용 필요 없음
     */
    public List<Order> findAllWithMemberDelivery() {
        return em.createQuery(
                "select o" +
                        " from Order o" +
                        " join fetch o.member m" + // to one 관계
                        " join fetch o.delivery d", Order.class) // to one 관계
                .getResultList();
    }

    /**
     * orders 예시 (x to many)
     * <p>
     * X to Many 일 경우는 distinct 사용
     */
    public List<Order> findAllWithItem() {
        // jpql distinct를 통해 order(master)의 중복 레코드 발생을 막는다.
        // 페이징 사용 불가
        return em.createQuery(
                "select distinct o " +
                        " from Order o " +
                        " join fetch o.member m " + // to one 관계
                        " join fetch o.delivery d " + // to one 관계
                        " join fetch o.orderItems oi " + // to many 관계
                        " join fetch oi.item i", Order.class) // to many 관계
                .getResultList();
    }

    /**
     * orders 예시 (x to many) 페이징 처리
     * <p>
     * X to One 일 경우는 distinct 사용 필요 없음
     * <p>
     * 1. x to many 중 x to one에 부분만 조회한다.
     * 2. 나머지 many가 되는 collection은 hibernate.default_batch_fetch_size 를 통해 처리힌다.
     */
    public List<Order> findAllWithMemberDelivery(int offset, int limit) {
        // findAllWithItem 에서 to one 관계만 남김
        return em.createQuery(
                "select o " +
                        " from Order o " +
                        " join fetch o.member m" + // to one 관계
                        " join fetch o.delivery d ", Order.class) // to one 관계
                .setFirstResult(offset)
                .setMaxResults(limit)
                .getResultList();
    }

}