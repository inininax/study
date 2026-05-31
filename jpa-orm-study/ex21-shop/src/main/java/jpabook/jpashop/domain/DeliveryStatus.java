package jpabook.jpashop.domain;

public enum DeliveryStatus {
    READY, COMP;

    public boolean isComp() {
        return this == COMP;
    }
}
