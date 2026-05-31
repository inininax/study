package study.jpa.domain.entity.embeddedid;

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
public class EdParent {
    @Id
    @GeneratedValue
    @Column(name = "parent_id")
    private long id;
    private String name;
}
