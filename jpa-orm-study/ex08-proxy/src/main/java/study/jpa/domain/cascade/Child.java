package study.jpa.domain.cascade;

import lombok.Getter;
import lombok.Setter;

import javax.persistence.*;

@Getter
@Setter
@Entity(name = "cascade_child")
@Table(name = "cascade_child")
public class Child {
    @Id
    @GeneratedValue
    private long id;

    private String name;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "parent_id")
    private Parent parent;

    public void changeParent(Parent parent) {
        if (this.parent != null) {
            this.parent.getChildList().remove(this);
        }
        this.parent = parent;
        parent.getChildList().add(this);
    }
}
