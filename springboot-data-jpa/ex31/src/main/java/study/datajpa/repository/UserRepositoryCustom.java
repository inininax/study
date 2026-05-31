package study.datajpa.repository;

import study.datajpa.domain.dto.UserCmd;
import study.datajpa.domain.dto.UserDto;

import java.util.List;

public interface UserRepositoryCustom {
    List<UserDto> findAllByCmd(UserCmd cmd);
}
