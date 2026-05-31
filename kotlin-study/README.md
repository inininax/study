# Kotlin study

## 코틀린에서 변수와 타입, 연산자를 다루는 방법

```text
    ?: Elvis 연산자
    ?. Safe call

    obj is Person
    obj !is Person
    val person = obj as? Person
    
    Any? 최상위
    Unit - Java의 void
    
    Nothing - 무조건 예외를 반환하는 함수, 무한 루프 함수 등
    fun fail(): Nothing {
        throw IllegalArgumentException()
    }
    
    "이름: ${person.name}, 이름2: $name"
    
    val withoutIndent =
        """
            ABC
            EFG
        """.trimIndent()
    println(withoutIndent)

    val str = "ABC"
    println(str[2])
    
    ==== 동일성 (java ==)
    == 동등성 (java equals)
    
    in , !in
    
    Lazy 연산
```

## 코틀린에서 코드를 제어하는 방법

```text
    if (조건) {}
    
    expression, statement
    
    switch, when
    
    for - in downTo step
    
    while
    
    Unchecked Exception
    
    .use{ x -> ... }
    
    default parameter
    
    named argument
    request("D", useNewLine = false)

    val array = arrayOf("A1", "B1", "C1")
    print2(*array)
    fun print2(vararg strings: String) {
        for (str in strings) {
            println(str)
        }
    }
```

## 코틀린에서의 OOP

```text
    Class
        

```

## 코틀린에서의 FP

## 추가적으로 알아두어야 할 코틀린 특성