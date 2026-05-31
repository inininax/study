package study.jpa.domain.joined;

import lombok.Getter;
import lombok.Setter;
import study.jpa.domain.BaseEntity;

import javax.persistence.*;

@Getter
@Setter
@Entity(name = "joined_item")
@Table(name = "joined_item")
@Inheritance(strategy = InheritanceType.JOINED)
public abstract class Item extends BaseEntity {
    @Id @GeneratedValue @Column(name = "item_id")
    private long id;
    private String name;
    private int price;
}