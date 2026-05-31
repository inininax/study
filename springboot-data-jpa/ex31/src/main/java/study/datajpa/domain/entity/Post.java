package study.datajpa.domain.entity;

import lombok.*;
import org.hibernate.envers.Audited;
import study.datajpa.domain.entity.base.BaseAudit;

import javax.persistence.*;

@Entity
@Audited
@Builder(access = AccessLevel.PROTECTED)
@AllArgsConstructor(access = AccessLevel.PROTECTED)
@NoArgsConstructor(access = AccessLevel.PROTECTED)
@Getter
public class Post extends BaseAudit {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Column(name = "post_id")
    private Long id;

    private String title;

    @Lob
    private String contents;

    public static Post create(String title, String contents) {
        return Post.builder().title(title).contents(contents).build();
    }
}
