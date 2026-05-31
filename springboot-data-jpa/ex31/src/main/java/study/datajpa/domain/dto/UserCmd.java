package study.datajpa.domain.dto;

import lombok.Builder;
import lombok.Data;

@Builder
@Data
public class UserCmd {
    private Long id;
    private String email;
    private String name;
    private String phone;
}