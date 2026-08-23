import org.jetbrains.kotlin.gradle.tasks.KotlinCompile

plugins {
    // KGP 1.9.24는 compileJava(JDK 21)와 jvmTarget 1.8의 불일치를 검증해 빌드가 실패한다 → 1.7.10 유지
    kotlin("jvm") version "1.7.10"
    application
}

group = "org.example"
version = "1.0-SNAPSHOT"

repositories {
    mavenCentral()
}

dependencies {
    testImplementation(kotlin("test"))
}

tasks.test {
    useJUnitPlatform()
}

tasks.withType<KotlinCompile> {
    kotlinOptions.jvmTarget = "1.8"
}

application {
    mainClass.set("MainKt")
}