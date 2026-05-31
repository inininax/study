package study.jpa.domain.singletable;

import lombok.Getter;
import lombok.Setter;
import study.jpa.domain.BaseEntity;

import javax.persistence.*;

@Getter
@Setter
@Entity(name = "singletable_item")
@Table(name = "singletable_item")
@Inheritance(strategy = InheritanceType.SINGLE_TABLE)
@DiscriminatorColumn(name = "dtype")
public abstract class Item extends BaseEntity {
    @Id @GeneratedValue @Column(name = "item_id")
    private long id;
    private String name;
    private int price;
}