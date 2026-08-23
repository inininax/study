package jpabook.jpashop.domain.entity;

import com.fasterxml.jackson.annotation.JsonIgnore;
import jpabook.jpashop.domain.entity.base.BaseEntity;
import jpabook.jpashop.domain.entity.embed.Address;
import jpabook.jpashop.domain.enums.DeliveryStatus;
import lombok.EqualsAndHashCode;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

import javax.persistence.*;

import static javax.persistence.FetchType.LAZY;

@Entity
@NoArgsConstructor
@Getter @Setter @EqualsAndHashCode
public class Delivery extends BaseEntity {
    @Id @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Column(name = "delivery_id")
    private Long id;

    @JsonIgnore // *중요 양방향 관계 시 무한 참조 방지를 위한 처리, 실사용 시에는 entity와 처리로직을 완전히 분리할 것
    @OneToOne(mappedBy = "delivery", fetch = LAZY)
    private Order order;

    // Address 는 @Embeddable 값 타입이므로 @Embedded 로 매핑한다 (기존 @Enumerated 는 enum 전용)
    @Embedded
    private Address address;

    @Enumerated(EnumType.STRING)
    private DeliveryStatus status;
}
