package com.example.study.ex09.java;

public class JavaPerson {
    private final String name;
    private int age;

    public JavaPerson(String name) {
        this(name, 1);
    }

    public JavaPerson(String name, int age) {
        if (age <= 0) {
            throw new IllegalArgumentException("Invalid age");
        }
        this.name = name;
        this.age = age;
    }

    public String getName() {
        return name;
    }

    public int getAge() {
        return age;
    }

    public void setAge(int age) {
        this.age = age;
    }
}
