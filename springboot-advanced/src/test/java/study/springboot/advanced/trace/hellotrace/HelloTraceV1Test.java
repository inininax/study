package study.springboot.advanced.trace.hellotrace;

import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.springframework.boot.test.system.CapturedOutput;
import org.springframework.boot.test.system.OutputCaptureExtension;
import study.springboot.advanced.trace.TraceId;
import study.springboot.advanced.trace.TraceStatus;

import java.util.Arrays;

import static org.assertj.core.api.Assertions.assertThat;


@ExtendWith(OutputCaptureExtension.class)
class HelloTraceV1Test {
    @Test
    void begin_end(CapturedOutput output) {
        HelloTraceV1 trace = new HelloTraceV1();
        TraceStatus status = trace.begin("hello");
        trace.end(status);

        String traceId = status.getTraceId().getId();
        // 레벨 0은 프리픽스 없이 "[traceId] message" 형식으로 남는다
        assertThat(output.getOut()).contains("[" + traceId + "] hello");
        assertThat(output.getOut()).contains("hello time=");
    }

    @Test
    void begin_exception(CapturedOutput output) {
        HelloTraceV1 trace = new HelloTraceV1();
        TraceStatus status = trace.begin("hello");
        trace.exception(status, new IllegalStateException());

        String traceId = status.getTraceId().getId();
        assertThat(output.getOut()).contains("[" + traceId + "] hello");
        assertThat(output.getOut()).contains("[" + traceId + "] hello time=");
        assertThat(output.getOut()).contains("ex=java.lang.IllegalStateException");
    }

    @Test
    void begin_end_level2(CapturedOutput output) {
        HelloTraceV1 trace = new HelloTraceV1();
        TraceStatus status1 = trace.begin("hello");

        // V1은 traceId를 파라미터로 받아 중첩하는 기능이 없으므로(V2의 beginSync 역할),
        // 반환된 TraceId로 다음 레벨을 직접 만들어 중첩을 시뮬레이션한다.
        TraceId nextTraceId = status1.getTraceId().createNextId();

        // 두 begin이 같은 trace-id를 공유하고 레벨만 증가하는지 검증
        assertThat(nextTraceId.getId()).isEqualTo(status1.getTraceId().getId());
        assertThat(nextTraceId.getLevel()).isEqualTo(status1.getTraceId().getLevel() + 1);

        TraceStatus status2 = new TraceStatus(nextTraceId, System.currentTimeMillis(), "hello2");
        trace.end(status2);
        trace.end(status1);

        // 레벨 1 프리픽스(|<--)와, 같은 trace-id가 두 로그에 모두 남았는지 확인
        assertThat(output.getOut()).contains("|<--hello2");
        long linesWithSameTraceId = Arrays.stream(output.getOut().split("\n"))
                .filter(line -> line.contains("[" + status1.getTraceId().getId() + "]"))
                .count();
        assertThat(linesWithSameTraceId).isGreaterThanOrEqualTo(2);
    }
}
