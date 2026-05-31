package study.jpa.domain.entity.idclass;

import lombok.*;

import java.io.Serializable;

@Getter
@Setter
@EqualsAndHashCode
@NoArgsConstructor
@AllArgsConstructor
public class IdChildPk implements Serializable {
    private long parent;
    private long id;
}
