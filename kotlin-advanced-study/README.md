# 코틀린 고급편 스터디

인프런 **[코틀린 고급편](https://www.inflearn.com/course/%EC%BD%94%ED%8B%80%EB%A6%B0-%EA%B3%A0%EA%B8%89%ED%8E%B8/dashboard)** 강의를 보며 실습/응용 코드를 작성하는 개인 스터디 저장소입니다.
강의 예제를 그대로 베끼기보다는 **코드를 직접 타이핑하고 변형**하면서 심화 개념을 체화하는 것을 목표로 합니다.

## Generic
### use-site variance
in, out 키워드를 통해 상속 관계에서 Generic Class의 관계 유지

공변 : co-variance, 함수 파라미터 입장에서 out 키워드가 붙을 경우 생산자, 공변 상태
반공변 : contra-variance, 함수 파라미터 입장에서 in 키워드가 붙을 경우 소비자, 반공변 상태

```kotlin
class Cage2<T> {
    private val animals: MutableList<T> = mutableListOf()

    fun getFirst(): T = animals.first()

    fun put(animal: T) {
        animals.add(animal)
    }

    fun moveFrom(otherCage: Cage2<out T>) {
        this.animals.addAll(otherCage.animals)
    }

    fun moveTo(otherCage: Cage2<in T>) {
        otherCage.animals.addAll(this.animals)
    }
}
```

상위 타입에 하위 타입 변수를 넣는 경우 또는 반대의 경우
```kotlin
fun main() {
    val cage1: Cage2<out Fish> = Cage2<GoldFish>()
    val cage2: Cage2<in GoldFish> = Cage2<Fish>()
}
```

### declaration-site variance
클래스 자체를 공변하게 선언
```kotlin
// 소비만 하는 클래스로 분리
class Cage4<in T> {
    private val animals: MutableList<T> = mutableListOf()

    fun put(animal: T) {
        this.animals.add(animal)
    }

    fun putAll(animals: List<T>) {
        this.animals.addAll(animals)
    }
}

// 생산만 하는 클래스로 분리
class Cage3<out T> {
    private val animals: MutableList<T> = mutableListOf()

    fun getFirst(): T = animals.first()

    fun getAll(): List<T> = animals.toList()
}
```

### 제약 generic constraints
Type에 대한 제약, Animal Type 및 Computable 구현에 대한 예시
```kotlin
class Cage5<T>(
    private val animals: MutableList<T> = mutableListOf()
) where T : Animal, T : Comparable<T> {}
```

### Type의 Nulla에 대한 제약
```kotlin
class Cage6<T : Any>
```

### 제네릭 함수 예시
```kotlin
fun <T> List<T>.hasIntersection(other: List<T>): Boolean {
    return (this.toSet() intersect other.toSet()).isNotEmpty()
}
```

### Type 소개와 Star Projection
java에서 generic 사용 시 type이 유실되기 때문에 kotlin에서는 reified 키워드를 사용해 구현
```kotlin
inline fun <reified T> List<*>.hasAnyInstanceOf(): Boolean {
    return this.any { it is T }
}

inline fun <reified T> List<*>.containsType() = this.firstOrNull { it is T } != null
```

---

## 지연과 위임
### lateinit과 lazy()
### by lazy의 원리와 위임 프로퍼티
### 코틀린의 표준 위임 객체
### 위임과 관련된 몇 가지 추가 기능
### Iterable과 Sequence (feat. JMH)

---

## 복잡한 함수형 프로그래밍
### 고차 함수와 함수 리터럴
### 복잡한 함수 타입과 고차 함수의 단점
### inline 함수 자세히 살펴보기
### SAM과 reference

---

## 연산자 오버로딩과 Kotlin DSL
### 연산자 오버로딩
### Kotlin DSL 직접 만들어보기
### DSL 활용 사례 살펴보기

---

## 어노테이션과 리플렉션
### 코틀린의 어노테이션
### 코틀린의 리플렉션
### 리플렉션 활용 - 나만의 DI 컨테이너 만들기
### 리플렉션 활용 - 타입 안전 이종 컨테이너와 슈퍼 타입 토큰

---

## 코틀린을 더 알아보자!
### 유용한 코틀린 표준 라이브러리 함수들
### 꼬리 재귀 함수와 인라인 클래스, multiple catch
### 유용한 k-도구들!!
