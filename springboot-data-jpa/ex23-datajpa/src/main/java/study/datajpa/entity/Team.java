package study.datajpa.entity;

import com.fasterxml.jackson.annotation.JsonIgnore;
import lombok.*;

import javax.persistence.*;
import java.util.ArrayList;
import java.util.List;

@Entity
@Getter @Setter @EqualsAndHashCode
@NoArgsConstructor(access = AccessLevel.PROTECTED) //기본 생성자 막고 싶은데, JPA 스팩상 PROTECTED로 열어두어야 함
@ToString(of = {"id", "name"})
public class Team extends BaseTimeEntity {
    @Id @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Column(name = "team_id")
    private Long id;
    private String name;

    //연관관계의 복잡도를 낮추기 위해 read-only로 사용
    @OneToMany(mappedBy = "team")
    @JsonIgnore
    List<Member> members = new ArrayList<>();

    public Team(String name) {
        this.name = name;
    }
}
