package study.springboot.advanced.config;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import study.springboot.advanced.trace.logtrace.LogTrace;
import study.springboot.advanced.trace.logtrace.ThreadLocalLogTrace;

@Configuration
public class LogTraceConfig {
    @Bean
    public LogTrace logTrace() {
        //return new FieldLogTrace(); //동시성 문제 발생
        return new ThreadLocalLogTrace();
    }
}
