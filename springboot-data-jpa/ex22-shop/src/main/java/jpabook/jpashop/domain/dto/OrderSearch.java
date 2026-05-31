package jpabook.jpashop.domain.dto;

import jpabook.jpashop.domain.enums.OrderStatus;
import lombok.EqualsAndHashCode;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

@NoArgsConstructor
@Getter @Setter @EqualsAndHashCode
public class OrderSearch {
    private String memberName;
    private OrderStatus orderStatus;
}
