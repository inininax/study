package example.jwt.domain.dto.res;

import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

@NoArgsConstructor
@Getter
@Setter
public class TokenDto {
    private String token;

    private TokenDto(String token) {
        this.token = token;
    }

    public static TokenDto from(String jwt) {
        return new TokenDto(jwt);
    }
}
