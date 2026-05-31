package study.jpa.domain.tableperclass;

import lombok.Getter;
import lombok.Setter;
import study.jpa.domain.BaseEntity;

import javax.persistence.*;

@Getter
@Setter
@Entity(name = "tableperclass_item")
@Table(name = "tableperclass_item")
@Inheritance(strategy = InheritanceType.TABLE_PER_CLASS)
public abstract class Item extends BaseEntity {
    @Id @GeneratedValue @Column(name = "item_id")
    private long id;
    private String name;
    private int price;
}