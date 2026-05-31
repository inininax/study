package study.jpa.domain;

import lombok.Getter;
import lombok.Setter;

import javax.persistence.*;
import java.util.ArrayList;
import java.util.List;

@Getter
@Setter
@Entity
@Table(name = "team")
public class Team {
    @Id
    @GeneratedValue(strategy = GenerationType.AUTO)
    private long id;

    @Column(length = 20, nullable = false)
    private String name;

    @OneToMany(mappedBy = "team") // Member.team - mappedBy 읽기만 가능
    private List<Member> members = new ArrayList<>();
}
