package study.jpa.domain.entity.embeddedid;

import lombok.EqualsAndHashCode;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

import javax.persistence.*;

@Getter
@Setter
@EqualsAndHashCode
@NoArgsConstructor
@Entity
public class EdChild {
    @EmbeddedId
    private EdChildPk id;

    @MapsId("parentId") // EdChildPk.parentId 매핑
    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "parent_id")
    private EdParent parent;

    private String name;
}
