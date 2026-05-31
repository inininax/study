package study.jpa.domain.entity;

import lombok.EqualsAndHashCode;
import lombok.Getter;
import lombok.Setter;

import javax.persistence.*;
import java.util.ArrayList;
import java.util.List;

@Getter
@Setter
@EqualsAndHashCode
@Entity
@NamedQueries(
        @NamedQuery(
                name = "Member.findByUsername",
                query = "select m from Member m where m.username = :username"
        )
)
public class Member {
    @Id
    @GeneratedValue
    @Column(name = "member_id")
    private long id;
    private String username;
    private int age;

    @Enumerated
    private Address address;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "team_id")
    private Team team;

    @OneToMany(mappedBy = "member")
    private List<Order> orders = new ArrayList<>();

    @Override
    public String toString() {
        return "Member{" +
                "id=" + id +
                ", username='" + username + '\'' +
                ", age=" + age +
                //", address=" + address +
                //", team=" + team +
                //", orders=" + orders +
                '}';
    }

    public void changeTeam(Team team) {
        if (this.team != null) {
            this.team.getMembers().remove(this);
        }
        this.team = team;
        team.getMembers().add(this);
    }
}
