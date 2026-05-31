package example.jwt.domain.entity;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import example.jwt.domain.entity.base.BaseEntity;
import example.jwt.domain.entity.embed.UserAuthorityId;
import lombok.*;

import javax.persistence.*;

@Entity
@NoArgsConstructor(access = AccessLevel.PROTECTED)
@Getter
@EqualsAndHashCode(exclude = {"user", "authority"})
@ToString(exclude = {"user", "authority"})
@JsonIgnoreProperties(value = {"user", "authority"})
public class UserAuthority extends BaseEntity {
    @EmbeddedId
    private UserAuthorityId id;

    @Column(nullable = false)
    private boolean activated;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "user_id")
    @MapsId("userId")
    private User user;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "authority_id")
    @MapsId("authorityId")
    private Authority authority;

    private UserAuthority(User user, Authority authority, boolean activated) {
        this.id = new UserAuthorityId(user, authority);
        this.activated = activated;
        this.user = user;
        this.authority = authority;

        user.addUserAuthority(this);
        authority.addUserAuthority(this);
    }

    public static UserAuthority create(User user, Authority authority, boolean activated) {
        return new UserAuthority(user, authority, activated);
    }

    public void beforeRemove() {
        this.user.removeUserAuthority(this);
        this.authority.removeUserAuthority(this);
    }
}
