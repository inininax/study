package study.jpa.domain.singletable;

import lombok.Getter;
import lombok.Setter;

import javax.persistence.DiscriminatorValue;
import javax.persistence.Entity;
import javax.persistence.Table;


@Getter
@Setter
@Entity(name = "singletable_book")
@Table(name = "singletable_book")
@DiscriminatorValue("BOOK")
public class Book extends Item {
    private String author;
    private String isbn;
}
