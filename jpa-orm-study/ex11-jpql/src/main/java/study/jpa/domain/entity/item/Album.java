package study.jpa.domain.entity.item;

import lombok.Getter;
import lombok.Setter;

import javax.persistence.DiscriminatorValue;
import javax.persistence.Entity;

@Getter
@Setter
@Entity
@DiscriminatorValue("ALBUM")
public class Album extends Item {
    private String artist;
    private String etc;
}
