package example.jwt.api;

import example.jwt.domain.entity.User;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import javax.persistence.EntityManager;
import java.util.List;

@RestController
@RequestMapping("/api")
@RequiredArgsConstructor
public class HelloController {

    private final EntityManager em;

    @GetMapping("/hello")
    public ResponseEntity<List<User>> hello() {
        return ResponseEntity.ok(em.createQuery("select distinct u" +
                " from User as u" +
                " left join fetch u.userAuthorities as ua" +
                " left join fetch ua.authority a" +
                " order by u.id desc", User.class).getResultList());
    }

}