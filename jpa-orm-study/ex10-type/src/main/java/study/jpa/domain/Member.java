package study.jpa.domain;

import lombok.Getter;
import lombok.Setter;

import javax.persistence.*;
import java.util.ArrayList;
import java.util.List;

@Getter
@Setter
@Entity
@Table(name = "member")
public class Member extends BaseEntity {
    @Id
    @GeneratedValue(strategy = GenerationType.AUTO)
    @Column(name = "member_id")
    private long id;

    private String name;

    @Embedded
    private Address address;

    // 필요 시 생성 (예제라 추가)
    @OneToMany(mappedBy = "member") // Order.member와 매핑
    private List<Order> orders = new ArrayList<>();
}
