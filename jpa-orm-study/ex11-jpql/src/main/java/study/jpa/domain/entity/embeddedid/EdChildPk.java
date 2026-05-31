package study.jpa.domain.entity.embeddedid;

import lombok.*;

import javax.persistence.Column;
import javax.persistence.Embeddable;
import javax.persistence.GeneratedValue;
import java.io.Serializable;

@Getter
@Setter
@EqualsAndHashCode
@NoArgsConstructor
@AllArgsConstructor
@Embeddable
public class EdChildPk implements Serializable {
    private long parentId; // @MapsId("parentId")로 매핑

    @GeneratedValue
    @Column(name = "child_id")
    private long id;

    public EdChildPk(EdParent parent) {
        this.parentId = parent.getId();
    }
}
