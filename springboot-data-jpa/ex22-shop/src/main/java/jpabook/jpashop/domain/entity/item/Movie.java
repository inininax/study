package jpabook.jpashop.domain.entity.item;

import jpabook.jpashop.domain.entity.Item;
import lombok.EqualsAndHashCode;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

import javax.persistence.DiscriminatorValue;
import javax.persistence.Entity;

@Entity
@DiscriminatorValue("MOVIE")
@NoArgsConstructor
@Getter @Setter @EqualsAndHashCode
public class Movie extends Item {
    private String director;
    private String actor;
}