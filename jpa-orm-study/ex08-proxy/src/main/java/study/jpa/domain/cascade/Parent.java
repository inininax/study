package study.jpa.domain.cascade;

import lombok.Getter;
import lombok.Setter;

import javax.persistence.*;
import java.util.ArrayList;
import java.util.List;

@Getter
@Setter
@Entity(name = "cascade_parent")
@Table(name = "cascade_parent")
public class Parent {
    @Id
    @GeneratedValue
    private long id;

    private String name;

    //@OneToMany(mappedBy = "parent", fetch = FetchType.LAZY, cascade = CascadeType.ALL) // cascade
    @OneToMany(mappedBy = "parent", fetch = FetchType.LAZY, cascade = CascadeType.ALL, orphanRemoval = true) // 고아객체
    private List<Child> childList = new ArrayList<>();

    public void addChild(Child child) {
        //child.changeParent(this);
        childList.add(child);
        child.setParent(this);
    }
}
