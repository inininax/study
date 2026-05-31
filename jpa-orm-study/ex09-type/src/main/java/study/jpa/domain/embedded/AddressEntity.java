package study.jpa.domain.embedded;

import lombok.Getter;
import lombok.Setter;

import javax.persistence.*;

@Getter
@Setter
@Entity(name = "address_entity")
@Table(name = "address_entity")
public class AddressEntity {
    @Id
    @GeneratedValue
    private long id;

    @Enumerated
    private Address address;

    public AddressEntity() {
    }

    public AddressEntity(String city, String street, String zipcode) {
        this.address = new Address(city, street, zipcode);
    }
}