package study.jpa.domain;

import lombok.Getter;
import lombok.Setter;

import javax.persistence.*;

/**
 * 1:N example
 * Owner가 Team일 경우
 */
@Getter
@Setter
@Entity
@Table(name = "one_to_many_member")
public class OneToManyMember {
    @Id
    @GeneratedValue(strategy = GenerationType.AUTO)
    @Column(name = "member_id")
    private long id;

    private String name;

    // OneToManyTeam이 Owner로 OneToManyTeam에 의해 team_id 생성됨
    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "team_id", insertable = false, updatable = false) // 양방향 사용 시 - 읽기 전용으로 설정
    private OneToManyTeam team;
}
