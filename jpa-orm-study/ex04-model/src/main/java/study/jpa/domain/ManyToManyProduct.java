package study.jpa.domain;

import lombok.Getter;
import lombok.Setter;

import javax.persistence.*;
import java.util.ArrayList;
import java.util.List;

/**
 * N:M example
 * 실무에서 사용하지 않음
 */
@Getter
@Setter
@Entity
@Table(name = "many_to_many_product")
public class ManyToManyProduct {
    @Id
    @GeneratedValue(strategy = GenerationType.AUTO)
    @Column(name = "product_id")
    private long id;

    @ManyToMany(mappedBy = "products") // ManyToManyMember.products
    List<ManyToManyMember> members = new ArrayList<>();
}
