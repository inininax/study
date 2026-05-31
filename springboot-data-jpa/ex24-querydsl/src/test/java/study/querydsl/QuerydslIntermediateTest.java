package study.querydsl;

import com.querydsl.core.BooleanBuilder;
import com.querydsl.core.Tuple;
import com.querydsl.core.types.ExpressionUtils;
import com.querydsl.core.types.Projections;
import com.querydsl.core.types.dsl.BooleanExpression;
import com.querydsl.core.types.dsl.Expressions;
import com.querydsl.jpa.JPAExpressions;
import lombok.extern.slf4j.Slf4j;
import org.junit.jupiter.api.Disabled;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import study.querydsl.dto.MemberDto;
import study.querydsl.dto.QMemberDto;
import study.querydsl.dto.UserDto;
import study.querydsl.entity.Member;
import study.querydsl.entity.QMember;

import java.util.List;

import static org.assertj.core.api.Assertions.assertThat;
import static study.querydsl.entity.QMember.member;

@Slf4j
public class QuerydslIntermediateTest extends BaseTest {

    @Test
    void selectString() {
        List<String> result = queryFactory
                .select(member.username)
                .from(member)
                .fetch();

        for (String username : result) {
            log.debug("username = {}", username);
        }
    }

    @Test
    void selectTuple() {
        List<Tuple> result = queryFactory
                .select(member.username, member.age)
                .from(member)
                .fetch();

        for (Tuple tuple : result) {
            String username = tuple.get(member.username);
            Integer age = tuple.get(member.age);
            log.debug("username = {}, age = {}", username, age);
        }
    }

    @Test
    void selectJpql() {
        String sql = "select new study.querydsl.dto.MemberDto(m.username, m.age)" +
                " from Member m";

        List<MemberDto> result = em.createQuery(sql, MemberDto.class).getResultList();

        for (MemberDto memberDto : result) {
            log.debug("memberDto = {}", memberDto);
        }
    }

    //프로퍼티 접근 - Setter
    @Test
    void selectProjectionsSetter() {
        List<MemberDto> result = queryFactory
                .select(Projections.bean(MemberDto.class,
                        member.username,
                        member.age
                ))
                .from(member)
                .fetch();

        for (MemberDto memberDto : result) {
            log.debug("memberDto = {}", memberDto);
        }
    }

    //필드 직접 접근
    @Test
    void selectProjectionsFields() {
        List<MemberDto> result = queryFactory
                .select(Projections.fields(MemberDto.class,
                        member.username,
                        member.age
                ))
                .from(member)
                .fetch();

        for (MemberDto memberDto : result) {
            log.debug("memberDto = {}", memberDto);
        }
    }

    @Test
    void selectProjectionsFiledAlias() {
        QMember memberSub = new QMember("memberSub");
        List<UserDto> result = queryFactory
                .select(Projections.fields(UserDto.class,
                        member.username.as("name"),
                        ExpressionUtils.as(JPAExpressions
                                .select(memberSub.age.max())
                                .from(memberSub), "age")
                ))
                .from(member)
                .fetch();

        for (UserDto userDto : result) {
            log.debug("userDto = {}", userDto);
        }
    }

    @Test
    void selectProjectionsConstructor() {
        List<MemberDto> result = queryFactory
                .select(Projections.constructor(MemberDto.class,
                        member.username,
                        member.age))
                .from(member)
                .fetch();

        for (MemberDto memberDto : result) {
            log.debug("memberDto : {}", memberDto);
        }
    }

    //@QueryProjection 활용

    @Test
    @DisplayName("@QueryProjection 활용")
    void selectProjectionsAnnotation() {
        List<MemberDto> result = queryFactory
                .select(new QMemberDto(member.username, member.age))
                .from(member)
                .fetch();

        for (MemberDto memberDto : result) {
            log.debug("memberDto = {}", memberDto);
        }
    }

    //distinct

    @Test
    void distinct() {
        List<String> result = queryFactory.select(member.username).distinct()
                .from(member)
                .fetch();
        for (String username : result) {
            log.debug("username = {}", username);
        }
    }

    //dynamic query - 동적 쿼리 - BooleanBuilder 사용

    @Test
    void dynamicQuery_BooleanBuilder() {
        String usernameParam = "member1";
        Integer ageParam = 10;

        List<Member> result = searchMember1(usernameParam, ageParam);
        assertThat(result.size()).isEqualTo(1);
    }

    private List<Member> searchMember1(String usernameCond, Integer ageCond) {
        BooleanBuilder builder = new BooleanBuilder();
        if (usernameCond != null) {
            builder.and(member.username.eq(usernameCond));
        }
        if (ageCond != null) {
            builder.and(member.age.eq(ageCond));
        }
        return queryFactory
                .selectFrom(member)
                .where(builder)
                .fetch();
    }

    //

    @Test
    void dynamicQuery_WhereParam() {
        String usernameParam = "member1";
        Integer ageParam = 10;

        List<Member> result = searchMember2(usernameParam, ageParam);
        assertThat(result.size()).isEqualTo(1);
    }

    private List<Member> searchMember2(String usernameCond, Integer ageCond) {
        return queryFactory
                .selectFrom(member)
                .where(usernameEq(usernameCond), ageEq(ageCond))
                .fetch();
    }

    private BooleanExpression usernameEq(String usernameCond) {
        return usernameCond != null ? member.username.eq(usernameCond) : null;
    }

    private BooleanExpression ageEq(Integer ageCond) {
        return ageCond != null ? member.age.eq(ageCond) : null;
    }

    //수정, 삭제 벌크 연산

    @Test
    void execute_update_delete() {
        //대량 데이터 수정
        long count = queryFactory
                .update(member)
                .set(member.username, "비회원")
                .where(member.age.lt(20))
                .execute();

        log.debug("update 1 count: {}", count);

        //기존 숫자에 1 더하기
        count = queryFactory
                .update(member)
                .set(member.age, member.age.add(1))
                .execute();

        log.debug("update 2 count: {}", count);

        //삭제
        count = queryFactory
                .delete(member)
                .where(member.age.eq(11))
                .execute();

        log.debug("delete count: {}", count);
    }

    //functions

    @Test
    @Disabled
    void func() {
        //replace
        String result = queryFactory
                //.select(Expressions.stringTemplate("function('replace', {0}, {1}, {2})", member.username, "member", "M"))
                .select(Expressions.stringTemplate("replace({0},'  ','')", member.username))
                .from(member)
                .fetchFirst();

        log.debug("result: {}", result);

        //lower
        queryFactory
                .select(member.username)
                .from(member)
                .where(member.username.eq(Expressions.stringTemplate("function('lower', {0})", member.username)))
                .fetchFirst();
    }

}