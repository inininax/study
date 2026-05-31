package learn.springboot.reactive.basic;

import java.util.Observable;
import java.util.Observer;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

/**
 * 원문: https://www.youtube.com/watch?v=8fenTR3KOJo
 * <p>
 * 용어 구분
 * Gang Of Four (GOF) : Subject   <> Observer
 * Reactive stream    : Publisher <> Subscriber
 * <p>
 * Observer Pattern의 단점
 * 1. data를 모두 전송한 후 complete의 개념이 없음
 * 2. error bug가 아닌 네트워크 장애와 같은 예외에 대응이 어렵다 (별도로 구현해야함)
 */
@SuppressWarnings("deprecation")
public class ObserverPatternExample {

    static class IntObservable extends Observable implements Runnable {

        // Source -> Event/Data -> Observer
        @Override
        public void run() {
            for (int i = 1; i <= 10; i++) {
                // 항상 상태를 변경하고
                setChanged();

                // publisher | subject
                // 값을 Observer에게 전달, 값은 object (하도 예전에 나와서 lambda 이런 거 없음)
                notifyObservers(i);         // push - METHOD(DATA)
                // => int i = it.next();    // pull - DATA METHOD()
            }
        }

    }

    public static void main(String[] args) {
        /*Observer ob = new Observer() {
            @Override
            public void update(Observable o, Object arg) {
                System.out.println("ob1:" + arg);
            }
        };*/

        // subscriber 또는 observer
        Observer ob = (Observable o, Object arg) -> {
            System.out.println(Thread.currentThread().getName() + " " + arg);
        };

        // publisher 또는 subject : Observerable이 던진 이벤트를 Observer가 받아서 처리
        IntObservable io = new IntObservable();
        io.addObserver(ob);

        // case 1
        // io.run();

        // case 2 신규 쓰레드 생성
        ExecutorService es = Executors.newSingleThreadExecutor();
        es.execute(io);

        System.out.println(Thread.currentThread().getName() + " EXIT");
        es.shutdown();
    }

}