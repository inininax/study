package study.jpa.domain.joined;

import lombok.Getter;
import lombok.Setter;

import javax.persistence.Entity;
import javax.persistence.Table;


@Getter
@Setter
@Entity(name = "joined_movie")
@Table(name = "joined_movie")
public class Movie extends Item {
    private String director;
    private String actor;
}
