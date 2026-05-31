package study.jpa.domain.entity.idclass;

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
@IdClass(IdChildPk.class)
public class IdChild {
    @Id
    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "parent_id")
    private IdParent parent;

    @Id
    @GeneratedValue
    @Column(name = "child_id")
    private long id;

    private String name;

    public IdChild(IdParent parent, long id) {
        this.parent = parent;
        this.id = id;
    }
}
