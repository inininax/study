package study.jpa.domain.lazy;

import lombok.Getter;
import lombok.Setter;

import javax.persistence.*;

@Getter
@Setter
@Entity(name = "lazy_locker")
@Table(name = "lazy_locker")
public class Locker {
    @Id
    @GeneratedValue
    @Column(name = "locker_id")
    private long id;

    private String name;

    @OneToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "member_id")
    private Member member;

    public void changeMember(Member member) {
        if (this.member != null) {
            this.member.setLocker(null);
        }
        this.member = member;
        member.setLocker(this);
    }

}
