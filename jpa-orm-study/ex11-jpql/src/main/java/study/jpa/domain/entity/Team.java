package study.jpa.domain.entity;

import lombok.EqualsAndHashCode;
import lombok.Getter;
import lombok.Setter;
import org.hibernate.annotations.BatchSize;

import javax.persistence.*;
import java.util.ArrayList;
import java.util.List;

@Getter
@Setter
@EqualsAndHashCode
@Entity
public class Team {
    @Id
    @GeneratedValue
    @Column(name = "team_id")
    private long id;

    private String name;

    @BatchSize(size = 1000) // global 설정도 가능함 - <property name="hibernate.default_batch_fetch_size" value="1000"/>
    @OneToMany(mappedBy = "team")
    private List<Member> members = new ArrayList<>();

    @Override
    public String toString() {
        return "Team{" +
                "id=" + id +
                ", name='" + name + '\'' +
                //", members=" + members +
                '}';
    }
}
