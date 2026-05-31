package study.jpa.domain.entity;

import lombok.EqualsAndHashCode;
import lombok.Getter;
import lombok.Setter;

import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.GeneratedValue;
import javax.persistence.Id;

@Getter
@Setter
@EqualsAndHashCode
@Entity
public class Product {
    @Id
    @GeneratedValue
    @Column(name = "product_id")
    private long id;
    private String name;
    private int price;
    private int stockAmount;
}
