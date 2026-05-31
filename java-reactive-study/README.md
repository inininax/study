# java reactive study

## reactive streams
- https://github.com/reactive-streams/reactive-streams-jvm

```java
public interface Publisher<T> {
    public void subscribe(Subscriber<? super T> s);
}

// onSubscribe onNext* (onError | onComplete)?
public interface Subscriber<T> {
    public void onSubscribe(Subscription s);
    public void onNext(T t);
    public void onError(Throwable t);
    public void onComplete();
}

public interface Subscription {
    public void request(long n);
    public void cancel();
}

public interface Processor<T, R> extends Subscriber<T>, Publisher<R> {
}
```