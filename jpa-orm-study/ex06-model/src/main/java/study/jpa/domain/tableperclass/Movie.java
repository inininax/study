package study.jpa.domain.tableperclass;

import lombok.Getter;
import lombok.Setter;

import javax.persistence.DiscriminatorValue;
import javax.persistence.Entity;
import javax.persistence.Table;


@Getter
@Setter
@Entity(name = "tableperclass_movie")
@Table(name = "tableperclass_movie")
public class Movie extends Item {
    private String director;
    private String actor;
}
