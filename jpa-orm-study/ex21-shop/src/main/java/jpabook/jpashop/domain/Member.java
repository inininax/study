package jpabook.jpashop.domain;

import com.fasterxml.jackson.annotation.JsonIgnore;
import lombok.EqualsAndHashCode;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

import javax.persistence.*;
import java.util.ArrayList;
import java.util.List;

@Getter @Setter @EqualsAndHashCode @NoArgsConstructor
@Entity
public class Member extends BaseEntity {
    @Id @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Column(name = "member_id")
    private Long id;

    //@NotEmpty(message = "이름을 입력해 주세요.") - entity에 검증로직을 완전히 분리할 것
    private String name;

    @Embedded
    private Address address;

    @JsonIgnore // *중요 양방향 관계 시 무한 참조 방지를 위한 처리, 실사용 시에는 entity와 처리로직을 완전히 분리할 것
    @OneToMany(mappedBy = "member")
    private List<Order> orders = new ArrayList<>();
}
