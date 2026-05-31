package study.jpa.domain;

import lombok.Getter;
import lombok.Setter;

import javax.persistence.*;
import java.util.ArrayList;
import java.util.List;

@Getter
@Setter
@Entity
@Table(name = "item")
public class Item {
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
}
