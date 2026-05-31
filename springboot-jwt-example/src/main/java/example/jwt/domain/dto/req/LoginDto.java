package example.jwt.domain.dto.req;

import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.NonNull;
import lombok.Setter;

import javax.validation.constraints.Size;

@NoArgsConstructor
@Getter
@Setter
public class LoginDto {
    @NonNull
    @Size(min = 2, max = 50)
    private String username;

    @NonNull
    @Size(min = 2, max = 255)
    private String password;
}
