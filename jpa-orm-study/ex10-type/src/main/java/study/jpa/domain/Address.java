package study.jpa.domain;

import lombok.AllArgsConstructor;
import lombok.EqualsAndHashCode;
import lombok.Getter;
import lombok.NoArgsConstructor;

import javax.persistence.Column;
import javax.persistence.Embeddable;

@Getter
@NoArgsConstructor
@AllArgsConstructor
@EqualsAndHashCode
@Embeddable
public class Address {
    @Column(length = 20)
    private String city;
    @Column(length = 20)
    private String street;
    @Column(length = 20)
    private String zipcode;
}
