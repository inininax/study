package study.jpa;

import study.jpa.domain.*;
import study.jpa.domain.item.Album;
import study.jpa.domain.item.Book;
import study.jpa.domain.item.Movie;

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
            // address ==================================================
            // member ==================================================
            Member member = new Member();
            member.setName("Member A");
            member.setAddress(new Address("A", "B", "C"));
            em.persist(member);

            // items ==================================================
            Album album = new Album();
            album.setName("Album A");
            album.setPrice(100000);
            album.setStockQuantity(999);
            album.setArtist("led zeppelin");
            em.persist(album);

            Book book = new Book();
            book.setName("Book B");
            book.setPrice(100000);
            book.setStockQuantity(999);
            book.setAuthor("toby");
            em.persist(book);

            Movie movie = new Movie();
            movie.setName("Movie C");
            movie.setPrice(100000);
            movie.setStockQuantity(999);
            movie.setDirector("dddd");
            em.persist(movie);

            // order items 1, 2 ==================================================
            OrderItem orderItem1 = new OrderItem();
            //orderItem1.changeOrder(order1); // **
            orderItem1.changeItem(album); // **
            //em.persist(orderItem1);

            OrderItem orderItem2 = new OrderItem();
            //orderItem2.changeOrder(order1); // **
            orderItem2.changeItem(book); // **
            //em.persist(orderItem2);

            Order order1 = new Order();
            order1.setStatus(OrderStatus.ORDER);
            order1.setOrderDate(LocalDateTime.now());
            // order.setMember(member);
            // order.getMember().getOrders().add(order);
            order1.changeMember(member); // **
            order1.addOrderItem(orderItem1);
            order1.addOrderItem(orderItem2);
            em.persist(order1);

            // order items 3, 4 ==================================================
            OrderItem orderItem3 = new OrderItem();
            //orderItem3.changeOrder(order2); // **
            orderItem3.changeItem(album); // **
            //em.persist(orderItem3);

            OrderItem orderItem4 = new OrderItem();
            //orderItem4.changeOrder(order2); // **
            orderItem4.changeItem(movie); // **
            //em.persist(orderItem4);

            Order order2 = new Order();
            order2.setStatus(OrderStatus.ORDER);
            order2.setOrderDate(LocalDateTime.now());
            order2.changeMember(member); // **
            order2.addOrderItem(orderItem3);
            order2.addOrderItem(orderItem4);
            em.persist(order2);

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
