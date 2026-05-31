package study.springboot.advanced.trace.threadlocal;

import lombok.extern.slf4j.Slf4j;
import org.junit.jupiter.api.Test;
import study.springboot.advanced.trace.threadlocal.code.ThreadLocalService;

@Slf4j
class ThreadLocalServiceTest {
    private ThreadLocalService threadLocalService = new ThreadLocalService();

    @Test
    void field() {
        log.info("main start");
        Runnable userA = () -> threadLocalService.logic("userA");
        Thread threadA = new Thread(userA);
        threadA.setName("thread-A");

        Runnable userB = () -> threadLocalService.logic("userB");
        Thread threadB = new Thread(userB);
        threadB.setName("thread-B");

        threadA.start();
        //sleep(2000);
        sleep(100);
        threadB.start();

        sleep(3000);
        log.info("main exit");
    }

    private void sleep(int millis) {
        try {
            Thread.sleep(millis);
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
    }
}