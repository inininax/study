package study.jpa;

import study.jpa.domain.embedded.Address;
import study.jpa.domain.embedded.AddressEntity;
import study.jpa.domain.embedded.Member;
import study.jpa.domain.embedded.Period;

import javax.persistence.EntityManager;
import javax.persistence.EntityManagerFactory;
import javax.persistence.EntityTransaction;
import javax.persistence.Persistence;
import java.time.LocalDateTime;
import java.util.Arrays;

public class TypeMain {
    public static void main(String[] args) {
        EntityManagerFactory emf = Persistence.createEntityManagerFactory("hello");
        EntityManager em = emf.createEntityManager();
        EntityTransaction tx = em.getTransaction();
        tx.begin();

        try {
            Member member = new Member();
            member.setUsername("Member A");
            member.setWorkPeriod(new Period(LocalDateTime.now().minusDays(365L), LocalDateTime.now().plusDays(365)));
            member.setHomeAddress(new Address("city1", "street1", "zipcode1"));
            member.getFavoriteFoods().addAll(Arrays.asList("사과", "포도", "자두"));
            member.getAddressHistories().add(new Address("city0", "street", "zipcode"));
            em.persist(member);

            em.flush();
            em.clear();

            Member findMember = em.find(Member.class, member.getId());
            findMember.setHomeAddress(new Address("city2", "street2", "zipcode2"));

            findMember.getFavoriteFoods().remove("사과");
            findMember.getFavoriteFoods().add("귤");

            // 모두 delete 시킨 후 추가
            findMember.getAddressHistories().add(new Address("city3", "street", "zipcode"));
            findMember.getAddressHistories().add(new Address("city4", "street", "zipcode"));
            findMember.getAddressHistories().add(new Address("city5", "street", "zipcode"));
            findMember.getAddressHistories().add(new Address("city6", "street", "zipcode"));
            findMember.getAddressHistories().remove(new Address("city5", "street", "zipcode"));

            findMember.getWorkHistories().add(new AddressEntity("city3", "street", "zipcode"));
            findMember.getWorkHistories().add(new AddressEntity("city4", "street", "zipcode"));
            findMember.getWorkHistories().add(new AddressEntity("city5", "street", "zipcode"));
            findMember.getWorkHistories().add(new AddressEntity("city6", "street", "zipcode"));
            findMember.getWorkHistories().remove(new AddressEntity("city5", "street", "zipcode"));

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
