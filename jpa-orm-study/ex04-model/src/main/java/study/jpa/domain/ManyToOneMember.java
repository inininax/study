package study.jpa.domain;

import lombok.Getter;
import lombok.Setter;

import javax.persistence.*;

/**
 * N:1 example
 * Owner가 Member일 경우
 */
@Getter
@Setter
@Entity
@Table(name = "many_to_one_member")
public class ManyToOneMember {
    @Id
    @GeneratedValue(strategy = GenerationType.AUTO)
    @Column(name = "member_id")
    private long id;

    private String name;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "team_id")
    private ManyToOneTeam team;

    public void changeTeam(ManyToOneTeam team) {
        if (this.team != null) {
            this.team.getMembers().remove(this);
        }
        this.team = team;
        team.getMembers().add(this);
    }
}
