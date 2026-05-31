package study.jpa.domain;

import lombok.Getter;
import lombok.Setter;

import javax.persistence.*;

/**
 * 1:1 example
 */
@Getter
@Setter
@Entity
@Table(name = "one_to_one_locker")
public class OneToOneLocker {
    @Id
    @GeneratedValue(strategy = GenerationType.AUTO)
    @Column(name = "locker_id")
    private long id;

    private String name;

    /*
    // 객체 중심으로 Owner를 지정 - Member가 Owner일 경우
    @OneToOne(mappedBy = "locker") // OneToOneMember.locker
    private OneToOneMember member;
    */

    // 데이터베이스 중심으로 Owner를 지정 -Locker가 Owner일 경우
    @OneToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "member_id")
    private OneToOneMember member;

    public void changeMember(OneToOneMember member) {
        if (this.member != null) {
            this.member.setLocker(null);
        }
        this.member = member;
        member.setLocker(this);
    }
}
