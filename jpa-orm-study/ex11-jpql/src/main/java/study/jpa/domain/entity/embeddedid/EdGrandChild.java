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
public class EdGrandChild {
    @EmbeddedId
    private EdGrandChildPk id;

    @MapsId("childId") // EdGrandChildPk.childId 매핑
    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumns({
            @JoinColumn(name = "parent_id"),
            @JoinColumn(name = "childId"),
    })
    private EdChild child;

    private String name;
}
