package study.jpa.domain;

import lombok.Getter;
import lombok.Setter;

import javax.persistence.*;
import java.util.ArrayList;
import java.util.List;

/**
 * 1:N example
 * Owner가 Team일 경우
 */
@Getter
@Setter
@Entity
@Table(name = "one_to_many_team")
public class OneToManyTeam {
    @Id
    @GeneratedValue(strategy = GenerationType.AUTO)
    @Column(name = "team_id")
    private long id;

    private String name;

    // OneToManyTeam이 Owner로 OneToManyTeam에 의해 team_id 생성됨
    @OneToMany
    @JoinColumn(name = "team_id")
    private List<OneToManyMember> members = new ArrayList<>();
}
