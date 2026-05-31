package study.jpa;

import study.jpa.domain.singletable.Album;
import study.jpa.domain.singletable.Book;
import study.jpa.domain.singletable.Movie;

import javax.persistence.EntityManager;
import javax.persistence.EntityManagerFactory;
import javax.persistence.EntityTransaction;
import javax.persistence.Persistence;

public class SingleTableMain {
    public static void main(String[] args) {
        EntityManagerFactory emf = Persistence.createEntityManagerFactory("hello");
        EntityManager em = emf.createEntityManager();
        EntityTransaction tx = em.getTransaction();
        tx.begin();

        try {
            Album album = new Album();
            album.setName("album");
            album.setPrice(1000000);
            em.persist(album);

            Movie movie = new Movie();
            movie.setName("movie");
            movie.setPrice(2000000);
            em.persist(movie);

            Book book = new Book();
            book.setName("book");
            book.setPrice(2000000);
            em.persist(book);

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
