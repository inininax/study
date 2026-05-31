package study.kotlin.advanced.generic

fun main() {
    example1()
    example2()
    example3()
    example4()
    example5()
    example6()
    example7()
    example8()
}

/**
 * Generic Type의 Null에 대한 제약에 대한 예시
 *
 * class Cage6<T : Any> { }
 */
fun example8() {
    val cage1 = Cage6<String>()

    // Type argument is not within its bounds: must be subtype of 'Any'.
    //val cage2 = Cage6<String?>()
}

/**
 * Generic Type의 추가 기능까지 확장한 경우의 예시
 *
 * class Cage5<T>(
 *   private val animals: MutableList<T> = mutableListOf()
 * ) where T : Animal, T : Comparable<T> { }
 */
fun example7() {
    //Cage5<Int>()
    //Cage5<String>()
    //Cage5<Carp>()
    //Cage5<GoldFish>()

    val birds = mutableListOf(
        Eagle(),
        Sparrow(),
    )
    val cage = Cage5(birds)
    cage.printAfterSoring()
}

/**
 * 클래스 Type 자체에 in, out을 명시하여
 * 클래스 역할 자체를 분리한 경우의 예씨
 *
 * class Cage3<out T> {}
 * class Cage4<in T> {}
 */
fun example6() {
    val fishCage = Cage3<Fish>()
    val animalCage: Cage3<Animal> = fishCage

    //animalCage.put(참새) // 불가
}

/**
 * Generic 사용 시 상속에 대한 관계는 유지되지 않기 때문에
 * in, out 키워드를 사용하는 예시
 *
 * out 키워드는 생성자 역할만 가능
 * in 키워드는 소비자 역할만 가능
 *
 * Class TYPE에 명시한 경우의 예시
 * val cage1: Cage2<out Fish> = Cage2<GoldFish>()
 * val cage2: Cage2<in GoldFish> = Cage2<Fish>()
 */
fun example5() {
    // Initializer type mismatch: expected 'Cage2<Fish>', actual 'Cage2<GoldFish>'.
    val cage1: Cage2<out Fish> = Cage2<GoldFish>()
    val cage2: Cage2<in GoldFish> = Cage2<Fish>()
}

/**
 * Generic 사용 시 상속에 대한 관계는 유지되지 않기 때문에
 * in, out 키워드를 사용하는 예시
 *
 * out 키워드는 생성자 역할만 가능
 * in 키워드는 소비자 역할만 가능
 *
 * 함수 파라미터 입장에서 사용될 경우의 예시
 * fun moveFrom(otherCage: Cage2<out T>) {}
 * fun moveTo(otherCage: Cage2<in T>) {}
 */
fun example4() {
    val myCage = Cage2<Fish>()

    val goldFishCage = Cage2<GoldFish>()
    goldFishCage.put(GoldFish("금붕어"))

    // Argument type mismatch: actual type is 'Cage2<Fish>', but 'Cage2<GoldFish>' was expected.
    //goldFishCage.moveTo(myCage)

    /*
        // 함수 파라미터 입장에서
        // in 키워드가 붙을 경우 소비자, 반공변 상태
        fun moveTo(otherCage: Cage2<in T>) {
            otherCage.animals.addAll(this.animals)
        }
    */
    goldFishCage.moveTo(myCage)
}

/**
 * Generic 사용 시 상속에 대한 관계는 유지되지 않기 때문에
 * in, out 키워드를 사용하는 예시
 *
 * out 키워드는 생성자 역할만 가능
 * in 키워드는 소비자 역할만 가능
 *
 * 함수 파라미터 입장에서 사용될 경우의 예시
 * fun moveFrom(otherCage: Cage2<out T>) {}
 * fun moveTo(otherCage: Cage2<in T>) {}
 */
fun example3() {
    // Fish와 GoldFish 간의 무공변으로 인한 moveFrom 호출 시의 오류
    val goldFishCage = Cage2<GoldFish>()
    goldFishCage.put(GoldFish("금붕어"))

    val fishCage = Cage2<Fish>()

    // Argument type mismatch: actual type is 'Cage2<GoldFish>', but 'Cage2<Fish>' was expected.
    //fishCage.moveFrom(goldFishCage)

    /*
        함수 파라미터 입장에서 out 키워드가 붙을 경우 생산자, 공변 상태

        fun moveFrom(otherCage: Cage2<out T>) {
            // out 키워드는 생성자 역할만 가능
            // Type 안정성이 깨질 수 있기 때문에

            //otherCage.getFirst() // 허용
            //otherCage.put(this.getFirst()) // out keyword가 있을 경우 값을 넣는 것은 불가

            this.animals.addAll(otherCage.animals)
        }
    */
    fishCage.moveFrom(goldFishCage)

    val fish = fishCage.getFirst()
    println(fish.name)
}

/**
 * Generic 사용에 대한 예시
 * class Cage2<T> {}
 */
fun example2() {
    val cage = Cage2<Carp>()
    cage.put(Carp("잉어"))

    val carp = cage.getFirst()
    println(carp.name)
}

/**
 * Generic 미사용 시 Type Casting이 필요한 경우에 대한 예제
 */
fun example1() {
    val cage = Cage()
    cage.put(Carp("잉어"))

    // Initializer type mismatch: expected 'Carp', actual 'Animal'.
    //val carp: Carp = cage.getFirst()

    // 대안
    val carp: Carp = cage.getFirst() as? Carp
        ?: throw IllegalStateException("No carp in the cage")

    println(carp.name)
}
