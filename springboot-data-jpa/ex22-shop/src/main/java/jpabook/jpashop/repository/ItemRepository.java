package jpabook.jpashop.repository;

import jpabook.jpashop.domain.entity.Item;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Repository;

import javax.persistence.EntityManager;
import java.util.List;

@RequiredArgsConstructor
@Repository
public class ItemRepository {
    private final EntityManager em;

    public void save(Item item) {
        if (item.getId() == null) {
            em.persist(item);
        } else {
            // 사용을 권장하지 않음 -> 변경 감지를 사용할 것을 권장
            //
            // 준영속성 엔티티를 영속화한다.
            // 또는 영속성 엔티티를 찾아 준영속성 엔티티의 값으로 변경(merge)한다.
            // item 객체 중 생략된 필드가 있으면 null로 update되어 버린다.
            //
            // item은 영속되지 않음
            // findItem은 영속 상태
            Item findItem = em.merge(item);
        }
    }

    public Item findOne(Long id) {
        return em.find(Item.class, id);
    }

    public List<Item> findAll() {
        return em.createQuery("select i from Item i", Item.class)
                .getResultList();
    }
}
