package study.datajpa.repository;

import com.querydsl.core.types.dsl.BooleanExpression;
import com.querydsl.jpa.JPQLQueryFactory;
import lombok.RequiredArgsConstructor;
import org.springframework.util.StringUtils;
import study.datajpa.domain.dto.QUserDto;
import study.datajpa.domain.dto.UserCmd;
import study.datajpa.domain.dto.UserDto;

import java.util.List;

import static study.datajpa.domain.entity.QUser.user;

@RequiredArgsConstructor
public class UserRepositoryCustomImpl implements UserRepositoryCustom {
    private final JPQLQueryFactory queryFactory;

    @Override
    public List<UserDto> findAllByCmd(UserCmd cmd) {
        return queryFactory.select(new QUserDto(user))
                .from(user)
                .where(nameEq(cmd.getName()),
                        emailContainsIgnoreCase(cmd.getEmail()),
                        phoneEq(cmd.getPhone()))
                .fetch();
    }

    private BooleanExpression nameEq(String name) {
        return StringUtils.hasText(name) ? user.name.eq(name) : null;
    }

    private BooleanExpression emailEq(String email) {
        return StringUtils.hasText(email) ? user.email.eq(email) : null;
    }

    private BooleanExpression emailContainsIgnoreCase(String email) {
        return StringUtils.hasText(email) ? user.email.containsIgnoreCase(email) : null;
    }

    private BooleanExpression phoneEq(String phone) {
        return StringUtils.hasText(phone) ? user.phone.eq(phone) : null;
    }
}
