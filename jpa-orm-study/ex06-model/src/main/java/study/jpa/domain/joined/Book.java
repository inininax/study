package study.jpa.domain.joined;

import lombok.Getter;
import lombok.Setter;

import javax.persistence.Entity;
import javax.persistence.Table;


@Getter
@Setter
@Entity(name = "joined_book")
@Table(name = "joined_book")
public class Book extends Item {
    private String author;
    private String isbn;
}
