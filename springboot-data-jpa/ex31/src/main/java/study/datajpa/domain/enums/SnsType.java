package study.datajpa.domain.enums;

public enum SnsType implements Code {
    KAKAO("카카오"),
    NAVER("네이버"),
    GOOGLE("구글"),
    APPLE("애플"),
    FACEBOOK("페이스북");

    private String name;

    SnsType(String name) {
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
