package example.jwt.domain.entity.embed;

import example.jwt.domain.entity.Authority;
import example.jwt.domain.entity.User;
import lombok.*;

import javax.persistence.Column;
import javax.persistence.Embeddable;
import java.io.Serializable;

@Embeddable
@NoArgsConstructor(access = AccessLevel.PROTECTED)
@Getter
@EqualsAndHashCode
@ToString
public class UserAuthorityId implements Serializable {
    @Column(name = "user_id")
    private Long userId;

    @Column(name = "authority_id")
    private Long authorityId;

    public UserAuthorityId(User user, Authority authority) {
        this.userId = user.getId();
        this.authorityId = authority.getId();
    }
}
