package study.springboot.advanced.trace.strategy;

import lombok.extern.slf4j.Slf4j;
import org.junit.jupiter.api.Test;
import study.springboot.advanced.trace.strategy.code.strategy.ContextV2;
import study.springboot.advanced.trace.strategy.code.strategy.StrategyLogic1;
import study.springboot.advanced.trace.strategy.code.strategy.StrategyLogic2;

@Slf4j
public class ContextV2Test {
    @Test
    void strategyV1() {
        ContextV2 context = new ContextV2();
        context.execute(new StrategyLogic1());
        context.execute(new StrategyLogic2());
    }

    @Test
    void strategyV2V3() {
        ContextV2 context = new ContextV2();
        context.execute(() -> log.info("비즈니스 로직1 수행"));
        context.execute(() -> log.info("비즈니스 로직2 수행"));
    }
}
