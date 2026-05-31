package study.datajpa.domain.enums;

public enum TemrsType implements Code {
    PRIVACY("개인정보 처리방침"),
    SERVICE("서비스 이용약관");
    //개인정보 이용동의
    //본인확인 서비스 이용약관
    //고유식별 정보처리 동의
    //통신사 이용약관

    private String name;

    TemrsType(String name) {
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
