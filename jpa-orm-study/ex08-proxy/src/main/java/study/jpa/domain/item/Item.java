package study.jpa.domain.item;

import lombok.Getter;
import lombok.Setter;
import study.jpa.domain.BaseEntity;
import study.jpa.domain.Category;
import study.jpa.domain.OrderItem;

import javax.persistence.*;
import java.util.ArrayList;
import java.util.List;

@Getter
@Setter
@Entity
@Table(name = "item")
@Inheritance(strategy = InheritanceType.JOINED)
@DiscriminatorColumn
public abstract class Item extends BaseEntity {
    @Id
    @GeneratedValue(strategy = GenerationType.AUTO)
    @Column(name = "item_id")
    private long id;

    private String name;

    private int price;

    @Column(name = "stock_quantity")
    private int stockQuantity;

    // 연관 관계 필요 시 설정 (예제이므로 사용함)
    @OneToMany(mappedBy = "item") // OrderItem.item과 매핑
    private List<OrderItem> orderItems = new ArrayList<>();

    /*@OneToMany(mappedBy = "item") // CategoryItem.item
    private List<CategoryItem> CategoryItems = new ArrayList<>();*/
    // 예제를 위해 many to many 사용 - 실무에서 사용 안함
    @ManyToMany(mappedBy = "items") // Category.items
    private List<Category> categories = new ArrayList<>();
}
