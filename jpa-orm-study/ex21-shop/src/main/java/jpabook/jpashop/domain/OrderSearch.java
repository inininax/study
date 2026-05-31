package jpabook.jpashop.domain;

import lombok.EqualsAndHashCode;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

@Getter @Setter @EqualsAndHashCode @NoArgsConstructor
public class OrderSearch {
    private String memberName;
    private OrderStatus orderStatus;
}
