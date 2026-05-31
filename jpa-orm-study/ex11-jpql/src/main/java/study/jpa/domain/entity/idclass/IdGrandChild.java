package study.jpa.domain.entity.idclass;

import lombok.EqualsAndHashCode;
import lombok.Getter;
import lombok.Setter;

import javax.persistence.*;

@Getter
@Setter
@EqualsAndHashCode
@Entity
@IdClass(IdGrandChildPk.class)
public class IdGrandChild {
    @Id
    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumns({
            @JoinColumn(name = "parent_id", referencedColumnName = "parent_id"),
            @JoinColumn(name = "child_id", referencedColumnName = "child_id")
    })
    private IdChild child;

    @Id
    @GeneratedValue
    @Column(name = "grandchild_id")
    private long id;

    private String name;
}
