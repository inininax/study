package com.example.study.ex09.java;

public class JavaPenguin extends JavaAnimal implements JavaFlyable, JavaSwimable {
    private final int wingCount;

    public JavaPenguin(String species) {
        super(species, 2);
        this.wingCount = 2;
    }

    @Override
    public void move() {
        System.out.println("Java Penguin");
    }

    @Override
    public int getLegCount() {
        return super.getLegCount() + this.wingCount;
    }

    @Override
    public void act() {
        JavaSwimable.super.act();
        JavaFlyable.super.act();
    }

    @Override
    public void fly() {
    }
}
