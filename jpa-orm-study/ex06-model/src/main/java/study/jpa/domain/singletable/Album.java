package study.jpa.domain.singletable;

import lombok.Getter;
import lombok.Setter;

import javax.persistence.DiscriminatorValue;
import javax.persistence.Entity;
import javax.persistence.Table;


@Getter
@Setter
@Entity(name = "singletable_album")
@Table(name = "singletable_album")
@DiscriminatorValue("ALBUM")
public class Album extends Item {
    private String artist;
}
