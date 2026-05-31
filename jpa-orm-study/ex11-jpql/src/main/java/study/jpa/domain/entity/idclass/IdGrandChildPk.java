package study.jpa.domain.entity.idclass;

import lombok.*;

import java.io.Serializable;

@Getter
@Setter
@EqualsAndHashCode
@NoArgsConstructor
@AllArgsConstructor
public class IdGrandChildPk implements Serializable {
    private IdChild child;
    private long id;

    public IdGrandChildPk(long parentId, long childId, long id) {
        this.child = new IdChild(new IdParent(parentId), childId);
        this.id = id;
    }
}