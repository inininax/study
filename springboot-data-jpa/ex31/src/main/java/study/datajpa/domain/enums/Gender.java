package study.datajpa.domain.enums;

public enum Gender implements Code {
    M("남"),
    F("여");

    private String name;

    Gender(String name) {
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