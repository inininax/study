package learn.springboot.reactive.basic;

import java.util.Arrays;
import java.util.Iterator;
import java.util.concurrent.*; // CountDownLatch 포함

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
        CountDownLatch done = new CountDownLatch(1); // 스트림 완료(onComplete/onError) 신호

        // [데이터를 주는 쪽] Publisher  <- Observable
        Flow.Publisher publisher = new Flow.Publisher() {
            @Override
            public void subscribe(Flow.Subscriber subscriber) {
                Iterator<Integer> it = itr.iterator();

                // event driven
                subscriber.onSubscribe(new Flow.Subscription() { // 예약 구독
                    private volatile boolean cancelled = false; // request/cancel 다른 스레드에서 호출되므로 volatile

                    @Override
                    public void request(long n) {

                        // 비동기 결과
                        // es.execute(() -> {});
                        Future<?> f = es.submit(() -> {
                            int i = 0;
                            try {
                                // while (n-- > 0) {
                                while (i++ < n && !cancelled) { // 취소되면 펌프 루프 종료
                                    Integer next;
                                    synchronized (it) { // iterator를 여러 request 작업이 공유하므로 보호
                                        next = it.hasNext() ? it.next() : null;
                                    }
                                    if (next == null) {
                                        subscriber.onComplete();
                                        break;
                                    } else {
                                        subscriber.onNext(next);
                                    }
                                }
                            } catch (RuntimeException e) {
                                subscriber.onError(e);
                            }
                        });

                    }

                    @Override
                    public void cancel() {
                        cancelled = true; // 다음 루프 반복에서 펌프가 멈춘다
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
                done.countDown(); // 에러로도 스트림이 끝났음을 알린다
            }

            @Override
            public void onComplete() {
                System.out.println(Thread.currentThread().getName() + " : onComplete");
                done.countDown(); // 스트림 완료 신호
            }
        };

        publisher.subscribe(subscriber);

        // 완료 전에 shutdown하면 이후 request 작업 제출 시 RejectedExecutionException 발생
        if (!done.await(10, TimeUnit.SECONDS)) {
            // 취소 경로에서 터미널 콜백이 없으면 영원히 대기하지 않도록 타임아웃 처리
            System.out.println("⚠️ 타임아웃: 스트림이 10초 내 완료되지 않았습니다");
        } // onComplete/onError까지 대기
        es.shutdown();
    }

}