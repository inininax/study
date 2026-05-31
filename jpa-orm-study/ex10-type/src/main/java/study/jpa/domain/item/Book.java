package study.jpa.domain.item;

import lombok.Getter;
import lombok.Setter;

import javax.persistence.DiscriminatorValue;
import javax.persistence.Entity;
import javax.persistence.Table;

@Getter
@Setter
@Entity
@Table(name = "item_book")
@DiscriminatorValue("BOOK")
public class Book extends Item {
    private String author;
    private String isbn;
}
