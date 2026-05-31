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
@Table(name = "one_to_one_member")
public class OneToOneMember {
    @Id
    @GeneratedValue(strategy = GenerationType.AUTO)
    @Column(name = "member_id")
    private long id;

    private String name;

    /*
    // 객체 중심으로 Owner를 지정 -Member가 Owner일 경우
    @OneToOne
    @JoinColumn(name = "locker_id")
    private OneToOneLocker locker;

    public void changeLocker(OneToOneLocker locker) {
        this.locker = locker;
        locker.setMember(this);
    }
    */

    // 데이터베이스 중심으로 Owner를 지정 - Locker가 Owner일 경우
    @OneToOne(mappedBy = "member", fetch = FetchType.LAZY) // OneToOneLocker.member
    private OneToOneLocker locker;
}
