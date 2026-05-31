package example.jwt.domain.dto.res;

import example.jwt.domain.entity.User;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

import java.util.Set;
import java.util.stream.Collectors;

@NoArgsConstructor
@Getter
@Setter
public class UserDto {
    private Long id;
    private String username;
    private String name;
    private boolean activated;
    private Set<String> authorities;

    private UserDto(Long id, String username, String name, boolean activated, Set<String> authorities) {
        this.id = id;
        this.username = username;
        this.name = name;
        this.activated = activated;
        this.authorities = authorities;
    }

    public static UserDto from(User user) {
        return new UserDto(
                user.getId(),
                user.getUsername(),
                user.getName(),
                user.isActivated(),
                user.getUserAuthorities().stream()
                        .map(userAuthority -> userAuthority.getAuthority().getName())
                        .collect(Collectors.toSet())
        );
    }

    public static UserDto from(Long id) {
        UserDto userDto = new UserDto();
        userDto.setId(id);
        return userDto;
    }

}
