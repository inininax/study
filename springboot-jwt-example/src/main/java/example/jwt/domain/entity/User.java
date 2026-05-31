package example.jwt.domain.entity;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import example.jwt.domain.entity.base.BaseEntity;
import lombok.*;

import javax.persistence.*;
import java.util.HashSet;
import java.util.Set;

@Entity
@NoArgsConstructor(access = AccessLevel.PROTECTED)
@Getter
@EqualsAndHashCode(exclude = {"userAuthorities"})
@ToString(exclude = {"password", "userAuthorities"})
@JsonIgnoreProperties(value = {"password", "userAuthorities"})
public class User extends BaseEntity {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Column(name = "user_id")
    private Long id;

    @Column(length = 50, nullable = false, unique = true, updatable = false)
    private String username;

    @Column(nullable = false)
    private String password;

    @Column(length = 20, nullable = false)
    private String name;

    @Column(nullable = false)
    private boolean activated;

    @OneToMany(mappedBy = "user")
    private Set<UserAuthority> userAuthorities = new HashSet<>();

    private User(String username, String password, String name, boolean activated) {
        this.username = username;
        this.password = password;
        this.name = name;
        this.activated = activated;
    }

    public static User create(String username, String password, String name, boolean activated) {
        return new User(username, password, name, activated);
    }

    public void addUserAuthority(UserAuthority userAuthority) {
        if (this.userAuthorities.contains(userAuthority)) {
            return;
        }
        this.userAuthorities.add(userAuthority);
    }

    public void removeUserAuthority(UserAuthority userAuthority) {
        if (!this.userAuthorities.contains(userAuthority)) {
            return;
        }
        this.userAuthorities.remove(userAuthority);
    }

}
