package com.example.study.ex09.java;

public interface JavaFlyable {
    default void act() {
        System.out.println("JavaFlyable act");
    }
}
