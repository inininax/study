package study.datajpa.domain.dto;

import com.querydsl.core.annotations.QueryProjection;
import lombok.Data;
import study.datajpa.domain.entity.User;
import study.datajpa.domain.enums.Gender;
import study.datajpa.domain.enums.MobileCarrier;
import study.datajpa.domain.enums.Nationality;

import java.time.LocalDate;

@Data
public class UserDto {
    private Long id;
    private String email;
    private String name;
    private LocalDate birthday;
    private MobileCarrier mobileCarrier;
    private String phone;
    private Gender gender;
    private Nationality nationality;
    private String ci;
    private String di;

    @QueryProjection
    public UserDto(User user) {
        this.id = user.getId();
        this.email = user.getEmail();
        this.name = user.getName();
        this.birthday = user.getBirthday();
        this.mobileCarrier = user.getMobileCarrier();
        this.phone = user.getPhone();
        this.gender = user.getGender();
        this.nationality = user.getNationality();
        this.ci = user.getCi();
        this.di = user.getDi();
    }
}
