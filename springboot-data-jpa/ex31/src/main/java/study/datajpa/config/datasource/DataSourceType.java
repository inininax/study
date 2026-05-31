package study.datajpa.config.datasource;

public enum DataSourceType {
    MASTER, SLAVE;

    public static DataSourceType fromTransactionReadOnly(boolean readonly) {
        return readonly ? SLAVE : MASTER;
    }
}