package study.jpa.domain.joined;

import lombok.Getter;
import lombok.Setter;

import javax.persistence.Entity;
import javax.persistence.Table;


@Getter
@Setter
@Entity(name = "joined_album")
@Table(name = "joined_album")
public class Album extends Item {
    private String artist;
}
