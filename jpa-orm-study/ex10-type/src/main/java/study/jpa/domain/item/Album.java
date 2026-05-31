package study.jpa.domain.item;

import lombok.Getter;
import lombok.Setter;

import javax.persistence.DiscriminatorValue;
import javax.persistence.Entity;
import javax.persistence.Table;

@Getter
@Setter
@Entity
@Table(name = "item_album")
@DiscriminatorValue("ALBUM")
public class Album extends Item {
    private String artist;
    private String etc;
}
