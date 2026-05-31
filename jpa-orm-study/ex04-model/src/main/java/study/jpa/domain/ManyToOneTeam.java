package study.jpa.domain;

import lombok.Getter;
import lombok.Setter;

import javax.persistence.*;
import java.util.ArrayList;
import java.util.List;

/**
 * N:1 example
 * Owner가 Member일 경우
 */
@Getter
@Setter
@Entity
@Table(name = "many_to_one_team")
public class ManyToOneTeam {
    @Id
    @GeneratedValue(strategy = GenerationType.AUTO)
    @Column(name = "team_id")
    private long id;

    private String name;

    @OneToMany(mappedBy = "team") // Member.team - mappedBy 읽기만 가능
    private List<ManyToOneMember> members = new ArrayList<>();
}
