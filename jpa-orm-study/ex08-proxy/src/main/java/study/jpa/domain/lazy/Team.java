package study.jpa.domain.lazy;

import lombok.Getter;
import lombok.Setter;

import javax.persistence.*;
import java.util.ArrayList;
import java.util.List;

@Getter
@Setter
@Entity(name = "lazy_team")
@Table(name = "lazy_team")
public class Team {
    @Id
    @GeneratedValue
    @Column(name = "team_id")
    private long id;

    private String name;

    @OneToMany(mappedBy = "team") // Member.team - mappedBy 읽기만 가능
    private List<Member> members = new ArrayList<>();
}
