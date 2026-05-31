package com.example.study.ex04;

import org.jetbrains.annotations.NotNull;

public class JavaMoney implements Comparable<JavaMoney> {
    private final long amount;

    public JavaMoney(long amount) {
        this.amount = amount;
    }

    @Override
    public int compareTo(@NotNull JavaMoney o) {
        // 1: 주어진게 더 작은 경우
        // 0: 같은 경우
        // -1: 주어진 값이 더 큰 경우
        return Long.compare(this.amount, o.amount);
    }

    @NotNull
    public Object plus(@NotNull JavaMoney other) {
        return this.amount + other.amount;
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;

        JavaMoney javaMoney = (JavaMoney) o;

        return amount == javaMoney.amount;
    }

    @Override
    public int hashCode() {
        return (int) (amount ^ (amount >>> 32));
    }

    @Override
    public String toString() {
        return "JavaMoney{" +
                "amount=" + amount +
                '}';
    }
}
