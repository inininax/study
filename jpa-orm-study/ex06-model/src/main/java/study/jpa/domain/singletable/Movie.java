package study.jpa.domain.singletable;

import lombok.Getter;
import lombok.Setter;

import javax.persistence.DiscriminatorValue;
import javax.persistence.Entity;
import javax.persistence.Table;


@Getter
@Setter
@Entity(name = "singletable_movie")
@Table(name = "singletable_movie")
@DiscriminatorValue("MOVIE")
public class Movie extends Item {
    private String director;
    private String actor;
}
