package study.datajpa.domain.enums;

public enum MobileCarrier implements Code {
    SKT("SKT"),
    KT("KT"),
    LGU("LG U+"),
    MVNO("알뜰폰");

    private String name;

    MobileCarrier(String name) {
        this.name = name;
    }

    @Override
    public String getCode() {
        return this.name();
    }

    @Override
    public String getName() {
        return this.name;
    }
}
