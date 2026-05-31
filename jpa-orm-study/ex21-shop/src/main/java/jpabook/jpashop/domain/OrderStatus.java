package jpabook.jpashop.domain;

public enum OrderStatus {
    ORDER, CANCEL;

    public boolean isOrder() {
        return this == ORDER;
    }

    public boolean isCancel() {
        return this == CANCEL;
    }
}
