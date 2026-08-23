package example.jwt.jwt;

import example.jwt.domain.dto.res.UserDto;
import io.jsonwebtoken.*;
import io.jsonwebtoken.io.Decoders;
import io.jsonwebtoken.security.Keys;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.GrantedAuthority;
import org.springframework.security.core.authority.SimpleGrantedAuthority;
import org.springframework.security.core.userdetails.User;
import org.springframework.stereotype.Component;

import java.security.Key;
import java.util.Arrays;
import java.util.Collection;
import java.util.Date;
import java.util.stream.Collectors;

@Slf4j
@Component
public class TokenProvider {

    private static final String USER_ID_KEY = "id";
    private static final String AUTHORITIES_KEY = "auth";

    private final long tokenValidityInMilliseconds;
    private final Key key;

    public TokenProvider(@Value("${jwt.secret}") String secret,
                         @Value("${jwt.token-validity-in-seconds}") long tokenValidityInSeconds) {
        this.tokenValidityInMilliseconds = tokenValidityInSeconds * 1000;
        this.key = Keys.hmacShaKeyFor(Decoders.BASE64.decode(secret));
    }

    public String createToken(Authentication authentication) {
        String authorities = authentication.getAuthorities().stream()
                .map(GrantedAuthority::getAuthority)
                .collect(Collectors.joining(","));

        Date exp = new Date(System.currentTimeMillis() + this.tokenValidityInMilliseconds);

        return Jwts.builder()
                .setSubject(authentication.getName())
                .claim(AUTHORITIES_KEY, authorities)
                .claim(USER_ID_KEY, ((UserDto) authentication.getDetails()).getId())
                .signWith(key, SignatureAlgorithm.HS512)
                .setExpiration(exp)
                .compact();
    }

    /**
     * 서명/만료가 유효해도 필수 클레임(auth, id)이 없으면 인증으로 취급하지 않는다.
     * null 반환 시 호출부(JwtFilter)가 인증 정보를 저장하지 않아 기존 "토큰 없음" 경로와
     * 동일하게 401 로 처리된다.
     */
    public Authentication getAuthentication(String token) {
        Claims claims = Jwts.parserBuilder()
                .setSigningKey(key)
                .build()
                .parseClaimsJws(token)
                .getBody();

        Object authoritiesClaim = claims.get(AUTHORITIES_KEY);
        if (authoritiesClaim == null || claims.get(USER_ID_KEY) == null) {
            log.info("JWT 토큰에 필수 클레임({},{})이 없습니다.", AUTHORITIES_KEY, USER_ID_KEY);
            return null;
        }

        Collection<? extends GrantedAuthority> authorities = Arrays.stream(authoritiesClaim.toString().split(","))
                .map(SimpleGrantedAuthority::new)
                .collect(Collectors.toList());

        User principal = new User(claims.getSubject(), "", authorities);

        // jwt parse 성공 시 db 조회 없이 인증 성공으로 판단
        UsernamePasswordAuthenticationToken authentication = new UsernamePasswordAuthenticationToken(principal, token, authorities);
        authentication.setDetails(UserDto.from(Long.valueOf(String.valueOf(claims.get(USER_ID_KEY)))));
        return authentication;
    }

    public boolean validateToken(String token) {
        try {
            Jwts.parserBuilder().setSigningKey(key).build().parseClaimsJws(token);
            return true;
        } catch (io.jsonwebtoken.security.SecurityException | MalformedJwtException e) {
            log.info("잘못된 JWT 서명입니다.");
        } catch (ExpiredJwtException e) {
            log.info("만료된 JWT 토큰입니다.");
        } catch (UnsupportedJwtException e) {
            log.info("지원되지 않는 JWT 토큰입니다.");
        } catch (IllegalArgumentException e) {
            log.info("JWT 토큰이 잘못되었습니다.");
        }
        return false;
    }
}
