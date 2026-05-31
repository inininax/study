package jpabook.jpashop.domain.entity.item;

import jpabook.jpashop.domain.entity.Item;
import lombok.EqualsAndHashCode;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

import javax.persistence.DiscriminatorValue;
import javax.persistence.Entity;

@Entity
@DiscriminatorValue("ALBUM")
@NoArgsConstructor
@Getter @Setter @EqualsAndHashCode
public class Album extends Item {
    private String artist;
    private String etc;
}
