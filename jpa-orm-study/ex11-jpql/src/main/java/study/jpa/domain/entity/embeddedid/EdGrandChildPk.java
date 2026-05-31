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
public class EdGrandChildPk implements Serializable {
    private EdChildPk childId; // @MapsId("childId")로 매핑

    @GeneratedValue
    @Column(name = "grandchild_id")
    private long id;

    public EdGrandChildPk(EdChild child) {
        this.childId = child.getId();
    }
}
