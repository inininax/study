package study.jpa.domain.lazy;

import lombok.Getter;
import lombok.Setter;

import javax.persistence.*;

@Getter
@Setter
@Entity(name = "lazy_member")
@Table(name = "lazy_member")
public class Member {
    @Id
    @GeneratedValue
    @Column(name = "member_id")
    private long id;

    private String name;

    @ManyToOne(fetch = FetchType.LAZY) // ** FetchType.LAZY or FetchType.EAGER
    @JoinColumn(name = "team_id")
    private Team team;

    @OneToOne(mappedBy = "member", fetch = FetchType.LAZY)
    private Locker locker;

    public void changeTeam(Team team) {
        if (this.team != null) {
            this.team.getMembers().remove(this);
        }
        this.team = team;
        team.getMembers().add(this);
    }

    @Override
    public String toString() {
        return "Member{" +
                "id=" + id +
                ", name='" + name + '\'' +
                //무한로딩
                //", team=" + team +
                //", locker=" + locker +
                '}';
    }
}