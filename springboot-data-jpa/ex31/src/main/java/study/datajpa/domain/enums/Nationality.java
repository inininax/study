package study.datajpa.domain.enums;

public enum Nationality implements Code {
    L("내국인"),
    F("외국인");

    private String name;

    Nationality(String name) {
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