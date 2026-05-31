package study.jpa.domain.tableperclass;

import lombok.Getter;
import lombok.Setter;

import javax.persistence.DiscriminatorValue;
import javax.persistence.Entity;
import javax.persistence.Table;


@Getter
@Setter
@Entity(name = "tableperclass_album")
@Table(name = "tableperclass_album")
public class Album extends Item {
    private String artist;
}
