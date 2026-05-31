package study.datajpa.config.datasource;

import lombok.extern.slf4j.Slf4j;
import org.springframework.jdbc.datasource.lookup.AbstractRoutingDataSource;
import org.springframework.transaction.support.TransactionSynchronizationManager;

@Slf4j
public class DynamicRoutingDataSource extends AbstractRoutingDataSource {
    @Override
    protected Object determineCurrentLookupKey() {
        boolean currentTransactionReadOnly = TransactionSynchronizationManager.isCurrentTransactionReadOnly();
        log.debug("currentTransactionReadOnly: {}", currentTransactionReadOnly);
        return DataSourceType.fromTransactionReadOnly(currentTransactionReadOnly);
    }
}