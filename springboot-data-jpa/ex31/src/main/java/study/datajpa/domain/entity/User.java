package study.datajpa.domain.entity;

import lombok.*;
import org.hibernate.envers.Audited;
import study.datajpa.domain.entity.base.BaseDateAudit;
import study.datajpa.domain.enums.Gender;
import study.datajpa.domain.enums.MobileCarrier;
import study.datajpa.domain.enums.Nationality;

import javax.persistence.*;
import java.time.LocalDate;

@Entity
@Audited
@Builder(access = AccessLevel.PROTECTED)
@AllArgsConstructor(access = AccessLevel.PROTECTED)
@NoArgsConstructor(access = AccessLevel.PROTECTED)
@Getter
public class User extends BaseDateAudit {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Column(name = "user_id")
    private Long id;
    private String email;
    private String password;
    private String name;
    private LocalDate birthday;

    @Enumerated(EnumType.STRING)
    private MobileCarrier mobileCarrier;
    private String phone;

    @Enumerated(EnumType.STRING)
    private Gender gender;

    @Enumerated(EnumType.STRING)
    private Nationality nationality;
    private String ci;
    private String di;

    public static User create(String email) {
        return User.builder().email(email).build();
    }

    public static User dummy() {
        return User.builder().id(1L).build();
    }
}
