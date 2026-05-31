package study.jpa.domain.tableperclass;

import lombok.Getter;
import lombok.Setter;

import javax.persistence.DiscriminatorValue;
import javax.persistence.Entity;
import javax.persistence.Table;


@Getter
@Setter
@Entity(name = "tableperclass_book")
@Table(name = "tableperclass_book")
public class Book extends Item {
    private String author;
    private String isbn;
}