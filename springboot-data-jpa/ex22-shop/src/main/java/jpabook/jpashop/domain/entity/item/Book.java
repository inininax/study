package jpabook.jpashop.domain.entity.item;

import jpabook.jpashop.domain.entity.Item;
import lombok.EqualsAndHashCode;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

import javax.persistence.DiscriminatorValue;
import javax.persistence.Entity;

@Entity
@DiscriminatorValue("BOOK")
@NoArgsConstructor
@Getter @Setter @EqualsAndHashCode
public class Book extends Item {
    private String author;
    private String isbn;
}
