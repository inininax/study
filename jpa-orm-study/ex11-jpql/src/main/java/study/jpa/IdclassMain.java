package study.jpa;

import study.jpa.domain.entity.idclass.IdChild;
import study.jpa.domain.entity.idclass.IdGrandChild;
import study.jpa.domain.entity.idclass.IdGrandChildPk;
import study.jpa.domain.entity.idclass.IdParent;

import javax.persistence.EntityManager;
import javax.persistence.EntityManagerFactory;
import javax.persistence.EntityTransaction;
import javax.persistence.Persistence;

public class IdclassMain {
    public static void main(String[] args) {
        EntityManagerFactory emf = Persistence.createEntityManagerFactory("hello");
        EntityManager em = emf.createEntityManager();
        EntityTransaction tx = em.getTransaction();
        tx.begin();

        try {
            IdParent parent_01 = new IdParent();
            parent_01.setName("1");
            em.persist(parent_01);

            //
            IdChild child_0101 = new IdChild();
            child_0101.setParent(parent_01);
            child_0101.setName("1-1");
            em.persist(child_0101);

            IdGrandChild grandChild_010101 = new IdGrandChild();
            grandChild_010101.setChild(child_0101);
            grandChild_010101.setName("1-1-1");
            em.persist(grandChild_010101);

            IdGrandChild grandChild_010102 = new IdGrandChild();
            grandChild_010102.setChild(child_0101);
            grandChild_010102.setName("1-1-2");
            em.persist(grandChild_010102);

            IdGrandChild grandChild_010103 = new IdGrandChild();
            grandChild_010103.setChild(child_0101);
            grandChild_010103.setName("1-1-3");
            em.persist(grandChild_010103);

            //
            IdChild child_0102 = new IdChild();
            child_0102.setParent(parent_01);
            child_0102.setName("1-2");
            em.persist(child_0102);

            IdGrandChild grandChild_010201 = new IdGrandChild();
            grandChild_010201.setChild(child_0102);
            grandChild_010201.setName("1-2-1");
            em.persist(grandChild_010201);

            em.flush();
            em.clear();

            IdGrandChildPk grandChildPk = new IdGrandChildPk(1, 2, 3);
            IdGrandChild findGrandChild = em.find(IdGrandChild.class, grandChildPk);
            System.out.println("parent.name=" + findGrandChild.getChild().getParent().getName());

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