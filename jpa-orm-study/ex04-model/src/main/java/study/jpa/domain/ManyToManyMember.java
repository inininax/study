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
@Table(name = "many_to_many_member")
public class ManyToManyMember {
    @Id
    @GeneratedValue(strategy = GenerationType.AUTO)
    @Column(name = "member_id")
    private long id;

    @ManyToMany
    @JoinTable(name = "many_to_many_member_product")
    List<ManyToManyProduct> products = new ArrayList<>();
}
