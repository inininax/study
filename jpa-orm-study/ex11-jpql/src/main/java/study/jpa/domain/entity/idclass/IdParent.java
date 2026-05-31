package study.jpa.domain.entity.idclass;

import lombok.EqualsAndHashCode;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.GeneratedValue;
import javax.persistence.Id;

@Getter
@Setter
@EqualsAndHashCode
@NoArgsConstructor
@Entity
public class IdParent {
    @Id
    @GeneratedValue
    @Column(name = "parent_id")
    private long id;
    private String name;

    public IdParent(long id) {
        this.id = id;
    }
}
