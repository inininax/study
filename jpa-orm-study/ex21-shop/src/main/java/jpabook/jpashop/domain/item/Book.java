package jpabook.jpashop.domain.item;

import lombok.EqualsAndHashCode;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

import javax.persistence.DiscriminatorValue;
import javax.persistence.Entity;

@Getter @Setter @EqualsAndHashCode @NoArgsConstructor
@Entity @DiscriminatorValue("BOOK")
public class Book extends Item {
    private String author;
    private String isbn;
}
