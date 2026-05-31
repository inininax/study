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
@ToString(exclude = {"userAuthorities"})
@JsonIgnoreProperties(value = {"userAuthorities"})
public class Authority extends BaseEntity {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Column(name = "authority_id")
    private Long id;

    @Column(length = 20, nullable = false, unique = true)
    private String name;

    @Column(nullable = false)
    private boolean activated;

    @OneToMany(mappedBy = "authority")
    private Set<UserAuthority> userAuthorities = new HashSet<>();

    private Authority(String name, boolean activated) {
        this.name = name;
        this.activated = activated;
    }

    public static Authority create(String name, boolean activated) {
        return new Authority(name, activated);
    }

    public void addUserAuthority(UserAuthority userAuthority) {
        if (!this.userAuthorities.contains(userAuthority)) {
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