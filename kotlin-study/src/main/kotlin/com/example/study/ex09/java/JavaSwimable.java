package com.example.study.ex09.java;

public interface JavaSwimable {
    default void act() {
        System.out.println("JavaSwimable act");
    }

    // abstract
    void fly();
}