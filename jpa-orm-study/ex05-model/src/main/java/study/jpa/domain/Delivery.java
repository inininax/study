package study.jpa.domain;

import lombok.Getter;
import lombok.Setter;

import javax.persistence.*;

@Getter
@Setter
@Entity
@Table(name = "delivery")
public class Delivery {
    @Id
    @GeneratedValue(strategy = GenerationType.AUTO)
    @Column(name = "delivery_id")
    private long id;

    private String city;

    private String street;

    private String zipcode;

    @Enumerated(EnumType.STRING)
    private DeliveryStatus status;

    // 필요 시 생성 (예제라 추가)
    @OneToOne(mappedBy = "delivery", fetch = FetchType.LAZY) // Order.delivery에 매핑
    private Order order;
}
