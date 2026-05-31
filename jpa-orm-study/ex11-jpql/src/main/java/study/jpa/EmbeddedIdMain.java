package study.jpa;

import study.jpa.domain.entity.embeddedid.*;

import javax.persistence.EntityManager;
import javax.persistence.EntityManagerFactory;
import javax.persistence.EntityTransaction;
import javax.persistence.Persistence;

public class EmbeddedIdMain {
    public static void main(String[] args) {
        EntityManagerFactory emf = Persistence.createEntityManagerFactory("hello");
        EntityManager em = emf.createEntityManager();
        EntityTransaction tx = em.getTransaction();
        tx.begin();

        try {
            EdParent parent01 = new EdParent();
            parent01.setName("1");
            em.persist(parent01);

            EdChildPk child0101Pk = new EdChildPk(parent01.getId(), 1);
            //EdChildPk child0101Pk = new EdChildPk(parent01);
            EdChild child0101 = new EdChild();
            child0101.setId(child0101Pk);
            child0101.setName("1-1");
            child0101.setParent(parent01);
            em.persist(child0101);

            EdGrandChildPk grandChild010101Pk = new EdGrandChildPk(child0101Pk, 1);
            //EdGrandChildPk grandChild010101Pk = new EdGrandChildPk(child0101);
            EdGrandChild grandChild010101 = new EdGrandChild();
            grandChild010101.setId(grandChild010101Pk);
            grandChild010101.setName("1-1-1");
            grandChild010101.setChild(child0101);
            em.persist(grandChild010101);

            EdGrandChildPk grandChild010102Pk = new EdGrandChildPk(child0101Pk, 2);
            //EdGrandChildPk grandChild010102Pk = new EdGrandChildPk(child0101);
            EdGrandChild grandChild010102 = new EdGrandChild();
            grandChild010102.setId(grandChild010102Pk);
            grandChild010102.setName("1-1-2");
            grandChild010102.setChild(child0101);
            em.persist(grandChild010102);

            EdChildPk child0102Pk = new EdChildPk(parent01.getId(), 2);
            EdChild child0102 = new EdChild();
            child0102.setId(child0102Pk);
            child0102.setName("1-2");
            child0102.setParent(parent01);
            em.persist(child0102);

            EdGrandChildPk grandChild010201Pk = new EdGrandChildPk(child0102Pk, 1);
            EdGrandChild grandChild010201 = new EdGrandChild();
            grandChild010201.setId(grandChild010201Pk);
            grandChild010201.setName("1-2-1");
            grandChild010201.setChild(child0102);
            em.persist(grandChild010201);

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