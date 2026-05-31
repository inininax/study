package study.datajpa.repository;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import study.datajpa.BaseTest;
import study.datajpa.entity.Item;

class ItemRepositoryTest extends BaseTest {

    @Autowired
    ItemRepository itemRepository;

    @Test
    void save() {
        Item item = new Item("A");
        itemRepository.save(item);
    }

}