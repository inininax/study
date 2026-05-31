package learn.springboot.reactive.basic;

import java.util.Arrays;
import java.util.Iterator;
import java.util.concurrent.*;

/**
 * 원문: https://www.youtube.com/watch?v=8fenTR3KOJo
 * <p>
 * Publisher와 Subscriber의 기본을 이해하기 위한 코드
 * <p>
 * Publisher  <- Observable
 * Subscriber <- Observer
 */
public class PubSubFlowExample {

    public static void main(String[] args) throws InterruptedException {

        // 예시
        Iterable<Integer> itr = Arrays.asList(1, 2, 3, 4, 5, 6, 7, 8, 9, 10);
        ExecutorService es = Executors.newCachedThreadPool();

        // [데이터를 주는 쪽] Publisher  <- Observable
        Flow.Publisher publisher = new Flow.Publisher() {
            @Override
            public void subscribe(Flow.Subscriber subscriber) {
                Iterator<Integer> it = itr.iterator();

                // event driven
                subscriber.onSubscribe(new Flow.Subscription() { // 예약 구독
                    @Override
                    public void request(long n) {

                        // 비동기 결과
                        // es.execute(() -> {});
                        Future<?> f = es.submit(() -> {
                            int i = 0;
                            try {
                                // while (n-- > 0) {
                                while (i++ < n) {
                                    if (it.hasNext()) {
                                        subscriber.onNext(it.next());
                                    } else {
                                        subscriber.onComplete();
                                        break;
                                    }
                                }
                            } catch (RuntimeException e) {
                                subscriber.onError(e);
                            }
                        });

                    }

                    @Override
                    public void cancel() {
                        // 취소할 경우
                    }
                });
            }
        };

        // [구독자] Subscriber <- Observer
        Flow.Subscriber subscriber = new Flow.Subscriber() {
            Flow.Subscription subscription;
            int bufferSize = 2;

            @Override
            public void onSubscribe(Flow.Subscription subscription) {
                System.out.println(Thread.currentThread().getName() + " : onSubscribe");

                this.subscription = subscription;
                this.subscription.request(2); // Long.MAX_VALUE
            }

            @Override
            public void onNext(Object item) {
                System.out.println(Thread.currentThread().getName() + " : onNext : " + item);

                // 버퍼 예시
                if (--bufferSize <= 0) {
                    bufferSize = 2;
                    this.subscription.request(2);
                }
            }

            @Override
            public void onError(Throwable throwable) {
                System.out.println("onError : " + throwable.getMessage());
            }

            @Override
            public void onComplete() {
                System.out.println(Thread.currentThread().getName() + " : onComplete");
            }
        };

        publisher.subscribe(subscriber);

        es.awaitTermination(10, TimeUnit.HOURS);
        es.shutdown();
    }

}