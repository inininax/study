package study.jpa;

import study.jpa.domain.*;

import javax.persistence.EntityManager;
import javax.persistence.EntityManagerFactory;
import javax.persistence.EntityTransaction;
import javax.persistence.Persistence;
import java.time.LocalDateTime;

public class MappingMain {
    public static void main(String[] args) {
        EntityManagerFactory emf = Persistence.createEntityManagerFactory("hello");
        EntityManager em = emf.createEntityManager();
        EntityTransaction tx = em.getTransaction();
        tx.begin();

        try {
            Member member = new Member();
            member.setName("Member A");
            em.persist(member);

            Item item1 = new Item();
            item1.setName("Item A");
            em.persist(item1);

            Item item2 = new Item();
            item2.setName("Item B");
            em.persist(item2);

            Item item3 = new Item();
            item3.setName("Item C");
            em.persist(item3);

            Order order1 = new Order();
            order1.setStatus(OrderStatus.ORDER);
            order1.setOrderDate(LocalDateTime.now());
            // order.setMember(member);
            // order.getMember().getOrders().add(order);
            order1.changeMember(member); // **
            em.persist(order1);

            Order order2 = new Order();
            order2.setStatus(OrderStatus.ORDER);
            order2.setOrderDate(LocalDateTime.now());
            order2.changeMember(member); // **
            em.persist(order2);

            OrderItem orderItem1 = new OrderItem();
            orderItem1.changeOrder(order1); // **
            orderItem1.changeItem(item1); // **
            em.persist(orderItem1);

            OrderItem orderItem2 = new OrderItem();
            orderItem2.changeOrder(order1); // **
            orderItem2.changeItem(item2); // **
            em.persist(orderItem2);

            OrderItem orderItem3 = new OrderItem();
            orderItem3.changeOrder(order2); // **
            orderItem3.changeItem(item1); // **
            em.persist(orderItem3);

            OrderItem orderItem4 = new OrderItem();
            orderItem4.changeOrder(order2); // **
            orderItem4.changeItem(item3); // **
            em.persist(orderItem4);

            System.out.println("flush ==================================================");
            em.flush();
            //em.clear();

            System.out.println("find member ==================================================");
            Member findMember = em.find(Member.class, 1L); // select * from member

            if (findMember != null) {
                System.out.println("findMember id ==================================================");
                System.out.println("findMember id: " + findMember.getId());

                System.out.println("findMember orders 1 ==================================================");
                System.out.println("findMember orders: " + findMember.getOrders().size()); // select * from orders

                System.out.println("findMember orders 2 ==================================================");
                findMember.getOrders().forEach(o -> { // none sql
                    System.out.println("o.getOrderItems() ==================================================");
                    o.getOrderItems().forEach(oi -> { // loop 별 select * from order_item a left join item b on (a.item_id = b.item_id)
                        System.out.println("item_id: " + oi.getItem().getId());
                    });
                });
            } else {
                System.out.println("findMember is null");
            }

            System.out.println("commit ==================================================");
            tx.commit();

        } catch (Exception e) {
            tx.rollback();
            e.printStackTrace();
        } finally {
            em.close();
            emf.close();
        }
    }
}
