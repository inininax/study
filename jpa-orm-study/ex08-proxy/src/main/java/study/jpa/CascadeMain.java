package study.jpa;

import study.jpa.domain.cascade.Child;
import study.jpa.domain.cascade.Parent;

import javax.persistence.EntityManager;
import javax.persistence.EntityManagerFactory;
import javax.persistence.EntityTransaction;
import javax.persistence.Persistence;

public class CascadeMain {
    public static void main(String[] args) {
        EntityManagerFactory emf = Persistence.createEntityManagerFactory("hello");
        EntityManager em = emf.createEntityManager();
        EntityTransaction tx = em.getTransaction();
        tx.begin();

        try {
            Child child1 = new Child();
            Child child2 = new Child();

            Parent parent = new Parent();
            parent.setName("A");
            parent.addChild(child1);
            parent.addChild(child2);

            // ** cascade
            // 단일 엔티티에 종속적일 경우에만 사용하는 것을 권장한다. (다른 곳에서 Child를 사용하지 않을 때)
            // CascadeType를 사용해 하위 객체들을 자동으로 동시에 저장한다.
            em.persist(parent); // ** @OneToMany(mappedBy = "parent", cascade = CascadeType.ALL)
            //em.persist(child1);
            //em.persist(child2);

            em.flush();
            em.clear();

            System.out.println("find findParent ===");
            Parent findParent = em.find(Parent.class, parent.getId());

            // ** 고아 객체 : 연관관계가 끊어진 자식 엔티티를 자동으로 삭제
            // ** @OneToMany(mappedBy = "parent", orphanRemoval = true)

            // 단일 엔티티에 종속적일 경우에만 사용하는 것을 권장한다. (다른 곳에서 Child를 사용하지 않을 때)
            // CascadeType를 사용해 하위 객체들을 자동으로 동시에 저장한다.
            System.out.println("remove child 0 ===");
            findParent.getChildList().remove(0); // 연관관계가 끊어지면서 delete from child where id = ? 실행

            em.flush();
            //em.clear();

            // child + parent 모두 삭제
            System.out.println("remove findParent ===");
            em.remove(findParent); // CascadeType.REMOVE 처럼 동작한다.

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
