package study.springboot.advanced.trace.logtrace;

import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.springframework.boot.test.system.CapturedOutput;
import org.springframework.boot.test.system.OutputCaptureExtension;
import study.springboot.advanced.trace.TraceStatus;

import java.util.Arrays;
import java.util.concurrent.CountDownLatch;
import java.util.concurrent.atomic.AtomicReference;
import java.util.stream.Stream;

import static org.assertj.core.api.Assertions.assertThat;

@ExtendWith(OutputCaptureExtension.class)
class FieldLogTraceTest {

    FieldLogTrace trace = new FieldLogTrace();

    @Test
    void begin_end_level2() {
        TraceStatus status1 = trace.begin("hello1");
        TraceStatus status2 = trace.begin("hello2");
        trace.end(status2);
        trace.end(status1);
    }

    @Test
    void begin_exception_level2() {
        TraceStatus status1 = trace.begin("hello1");
        TraceStatus status2 = trace.begin("hello2");
        trace.exception(status2, new IllegalStateException());
        trace.exception(status1, new IllegalStateException());
    }

    /**
     * Field 기반 traceIdHolder의 동시성 문제를 재현하는 레이스 데모.
     * 두 스레드가 하나의 FieldLogTrace를 공유하면 트레이스가 섞이거나 예외가 발생한다.
     */
    @Test
    void concurrency_race_demo(CapturedOutput output) throws InterruptedException {
        final int attempts = 30; // 레이스는 확률적이므로 여러 라운드 반복
        int anomalies = 0;

        for (int attempt = 0; attempt < attempts; attempt++) {
            FieldLogTrace raceTrace = new FieldLogTrace(); // 라운드마다 새 인스턴스
            CountDownLatch gate = new CountDownLatch(2); // 두 스레드 동시 출발 게이트
            AtomicReference<Throwable> failure = new AtomicReference<>();

            Runnable taskA = () -> runSequence(raceTrace, gate, failure, "taskA");
            Runnable taskB = () -> runSequence(raceTrace, gate, failure, "taskB");

            Thread threadA = new Thread(taskA, "thread-A");
            Thread threadB = new Thread(taskB, "thread-B");
            threadA.start();
            threadB.start();
            threadA.join();
            threadB.join();

            if (failure.get() != null) {
                anomalies++;
            }
        }

        // 이상 징후 1: 작업에서 예외 발생 (traceIdHolder 경합으로 NPE 등)
        // 이상 징후 2: 첫 레벨 begin인데 "|-->"(중첩 프리픽스)로 남은 로그
        long misNestedFirstLevelLogs = firstLevelStartLines(output.getOut())
                .filter(line -> line.contains("|"))
                .count();

        assertThat(anomalies + (int) misNestedFirstLevelLogs).isGreaterThanOrEqualTo(1);
    }

    private void runSequence(FieldLogTrace trace, CountDownLatch gate, AtomicReference<Throwable> failure, String name) {
        try {
            gate.countDown();
            gate.await(); // 두 스레드가 최대한 동시에 진입

            TraceStatus status1 = trace.begin(name);
            TraceStatus status2 = trace.begin(name + "2");
            trace.end(status2);
            trace.end(status1);
        } catch (Exception e) {
            failure.compareAndSet(null, e);
        }
    }

    private Stream<String> firstLevelStartLines(String logOutput) {
        // 첫 레벨 begin 로그는 메시지("taskA"/"taskB")로 끝난다. 중첩 begin은 "taskA2"로 끝난다.
        return Arrays.stream(logOutput.split("\n"))
                .filter(line -> line.endsWith("taskA") || line.endsWith("taskB"));
    }
}
