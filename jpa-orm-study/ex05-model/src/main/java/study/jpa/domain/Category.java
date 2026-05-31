package study.jpa.domain;

import lombok.Getter;
import lombok.Setter;

import javax.persistence.*;
import java.util.ArrayList;
import java.util.List;

@Getter
@Setter
@Entity
@Table(name = "category")
public class Category {
    @Id
    @GeneratedValue(strategy = GenerationType.AUTO)
    @Column(name = "category_id")
    private long id;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "parent_id") // self join
    private Category parent;

    private String name;

    @OneToMany(mappedBy = "parent")
    private List<Category> child = new ArrayList<>();

    /*@OneToMany(mappedBy = "category") // CategoryItem.category
    private List<CategoryItem> CategoryItems = new ArrayList<>();*/
    // 예제를 위해 many to many 사용 - 실무에서 사용 안함
    @ManyToMany
    @JoinTable(
            name = "category_item", // category_item 중계 테이블 생성
            joinColumns = @JoinColumn(name = "category_id"), // 내가 조인할 컬럼
            inverseJoinColumns = @JoinColumn(name = "item_id") // 상대 테이블이 조인할 컬럼
    )
    private List<Item> items = new ArrayList<>();
}
