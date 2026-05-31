package study.jpa.domain.embedded;

import javax.persistence.Column;
import javax.persistence.Embeddable;
import java.util.Objects;

/**
 * 값 타입은 참조 시 오류 가능성이 커지기 때문에 getter만 생성한다.
 */
//@Getter
//@EqualsAndHashCode
//@NoArgsConstructor
//@AllArgsConstructor
@Embeddable
public class Address {
    private String city;
    private String street;
    @Column(name = "ZIPCODE", length = 50)
    private String zipcode;

    public Address() {
    }

    public Address(String city, String street, String zipcode) {
        this.city = city;
        this.street = street;
        this.zipcode = zipcode;
    }

    public String getCity() {
        return city;
    }

    public String getStreet() {
        return street;
    }

    public String getZipcode() {
        return zipcode;
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        Address address = (Address) o;
        return Objects.equals(city, address.city) && Objects.equals(street, address.street) && Objects.equals(zipcode, address.zipcode);
    }

    @Override
    public int hashCode() {
        return Objects.hash(city, street, zipcode);
    }
}