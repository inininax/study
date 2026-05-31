package jpabook.jpashop.domain.entity.embed;

import lombok.*;

import javax.persistence.Embeddable;

@Embeddable
@NoArgsConstructor
@AllArgsConstructor
@Getter @Setter @EqualsAndHashCode
public class Address {
    private String city;
    private String street;
    private String zipcode;
}
