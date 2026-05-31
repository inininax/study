package jpabook.jpashop.service;

import jpabook.jpashop.StringTestSupport;
import jpabook.jpashop.domain.Address;
import jpabook.jpashop.domain.Member;
import jpabook.jpashop.domain.Order;
import jpabook.jpashop.domain.OrderStatus;
import jpabook.jpashop.domain.item.Book;
import jpabook.jpashop.domain.item.Item;
import jpabook.jpashop.exception.NoEnoughStockException;
import jpabook.jpashop.repository.OrderRepository;
import org.junit.jupiter.api.Disabled;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.transaction.annotation.Transactional;

import javax.persistence.EntityManager;
import javax.persistence.PersistenceContext;
import java.time.LocalDateTime;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;
import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

@Transactional
class OrderServiceTest extends StringTestSupport {

    @PersistenceContext EntityManager em;
    @Autowired OrderService orderService;
    @Autowired OrderRepository orderRepository;

    @Test
    @DisplayName("상품 주문")
    void order() {
        //given
        Member member = createMember();
        Item item = createBook("jpa", 30000, 10);
        int orderCount = 2;

        //when
        Long orderId = orderService.order(member.getId(), item.getId(), orderCount);

        //then
        Order findOrder = orderRepository.findOne(orderId);

        assertThat(findOrder.getStatus()).isEqualTo(OrderStatus.ORDER).as("상품 주문시 상태는 ORDER");
        assertThat(findOrder.getOrderItems().size()).isEqualTo(1).as("주문한 상품 종류 수가 정확해야 한다.");
        assertThat(findOrder.getTotalPrice()).isEqualTo(30000 * 2).as("주문 가격은 가격 * 수량이다.");
        assertThat(item.getStockQuantity()).isEqualTo(10 - 2).as("주문 수량만큼 재고가 줄어야 한다.");
    }

    @Test
    @DisplayName("상품 주문 재고수량 초과")
    void noEnoughStockException() {
        //given
        Member member = createMember();
        Item item = createBook("jpa", 10000, 10);
        int orderCount = 11;

        //when + then
        assertThatThrownBy(() -> orderService.order(member.getId(), item.getId(), orderCount))
                .isInstanceOf(NoEnoughStockException.class)
                .as("재고 수량 부족 예외가 발생해야 한다.");
    }

    @Disabled
    @Test
    @DisplayName("주문 취소")
    void cancel() {
        //given
        Member member = createMember();
        Item item = createBook("jpa", 10000, 10);
        int orderCount = 2;
        Long orderId = orderService.order(member.getId(), item.getId(), orderCount);

        //when
        orderService.cancelOrder(orderId);

        //then
        Order findOrder = orderRepository.findOne(orderId);

        assertTrue(findOrder.getStatus().isCancel());
        assertEquals(item.getStockQuantity(), 10);
    }

    private Member createMember() {
        Member member = new Member();
        member.setName("Test");
        member.setAddress(new Address("AAA", "BBB", "12345"));
        member.setCreatedBy(member.getId());
        member.setCreatedDate(LocalDateTime.now());
        em.persist(member);
        return member;
    }

    private Book createBook(String name, int price, int stockQuantity) {
        Book book = new Book();
        book.setName(name);
        book.setStockQuantity(stockQuantity);
        book.setPrice(price);
        em.persist(book);
        return book;
    }

}