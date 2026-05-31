package study.kotlin.advanced.generic


inline fun <reified T> printIfTypeMatch(item: Any) {
    if (item is T) {
        println(item)
    }
}

inline fun <reified T> List<*>.hasAnyInstanceOf(): Boolean {
    return this.any { it is T }
}

inline fun <reified T> List<*>.containsType() = this.firstOrNull { it is T } != null

fun example101() {
    val num = 3
    num.toSuperString()

    val str = "ABC"
    str.toSuperString()
    println("${str::class.java.name}: $str")
}

fun <T> T.toSuperString() {
    // Cannot use 'T' as reified type parameter. Use a class instead.
    // Cannot infer type for type parameter 'T'. Specify it explicitly.
    // <html>Unresolved reference. None of the following candidates is applicable because of a receiver type mismatch:<br/>val &lt;T&gt; KClass&lt;T&gt;.java: Class&lt;T&gt;

    //println("${T::class.java.name}: $this")
}

class TypeErase {
}