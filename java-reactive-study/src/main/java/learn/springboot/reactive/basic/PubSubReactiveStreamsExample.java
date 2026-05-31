package learn.springboot.reactive.basic;

import lombok.extern.slf4j.Slf4j;
import org.reactivestreams.Publisher;
import org.reactivestreams.Subscriber;
import org.reactivestreams.Subscription;

import java.util.Iterator;
import java.util.function.Function;
import java.util.stream.Stream;

/**
 * 원문: https://www.youtube.com/watch?v=DChIxy9g19o
 * <p>
 * Reactive Streams - Operators
 * <p>
 * Publisher -> Data1 -> Operators1 -> Data2 -> ... -> Operators999 -> Data999 -> Subscriber
 * <p>
 * 예제
 * 1. map (data1 -> function -> data2): map을 통해 데이터 가공
 * <p>
 * pub -> data1 -> mapPub -> data2 -> logSub (Down stream)
 * _____________<- subscribe(logSub) (Up stream)
 * _____________-> onSubscribe(s)
 * _____________-> onNext
 * _____________-> onNext
 * _____________-> onComplete
 */
@Slf4j
public class PubSubReactiveStreamsExample {

    public static void main(String[] args) {
        Publisher<Integer> pub = iterPub(Stream.iterate(1, i -> i < 10, i -> i + 1).iterator());
        Publisher<Integer> mapPub = mapPub(pub, s -> s * 10);
        Publisher<Integer> map2Pub = mapPub(mapPub, s -> -s);
        map2Pub.subscribe(logSub());
    }

    // Operator
    private static Publisher<Integer> mapPub(Publisher<Integer> pub, Function<Integer, Integer> f) {
        return new Publisher<Integer>() {
            @Override
            public void subscribe(Subscriber<? super Integer> sub) {
                pub.subscribe(new Subscriber<Integer>() {
                    @Override
                    public void onSubscribe(Subscription s) {
                        sub.onSubscribe(s);
                    }

                    @Override
                    public void onNext(Integer i) {
                        // apply function
                        sub.onNext(f.apply(i));
                    }

                    @Override
                    public void onError(Throwable t) {
                        sub.onError(t);
                    }

                    @Override
                    public void onComplete() {
                        sub.onComplete();
                    }
                });
            }
        };
    }

    private static Subscriber<Integer> logSub() {
        return new Subscriber<>() {
            @Override
            public void onSubscribe(Subscription s) {
                log.debug("onSubscribe: {}", s);
                s.request(Long.MAX_VALUE);
            }

            @Override
            public void onNext(Integer i) {
                log.debug("onNext: {}", i);
            }

            @Override
            public void onError(Throwable t) {
                log.debug("onError: {}", t);
            }

            @Override
            public void onComplete() {
                log.debug("onComplete");
            }
        };
    }

    private static Publisher<Integer> iterPub(Iterator<Integer> iter) {
        return new Publisher<>() {
            @Override
            public void subscribe(Subscriber<? super Integer> sub) {
                sub.onSubscribe(new Subscription() {
                    @Override
                    public void request(long n) {
                        try {
                            iter.forEachRemaining(i -> sub.onNext(i));
                            sub.onComplete();
                        } catch (Throwable t) {
                            sub.onError(t);
                        }
                    }

                    @Override
                    public void cancel() {
                    }
                });
            }
        };
    }

}