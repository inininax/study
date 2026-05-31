package learn.springboot.reactive.basic;

import java.util.Arrays;
import java.util.Iterator;
import java.util.List;

/**
 * 원문: https://www.youtube.com/watch?v=8fenTR3KOJo
 */
public class IterableExample {

    public static void main(String[] args) {
        List<Integer> list = Arrays.asList(1, 2, 3, 4, 5, 6);
        for (Integer i : list) {
            System.out.println(i);
        }

        Iterable<Integer> iter = Arrays.asList(1, 2, 3, 4, 5, 6);
        for (Integer i : iter) {
            System.out.println(i);
        }

        // Iterable을 통해 직접 구현
        Iterable<Integer> iter2 = new Iterable<Integer>() {
            @Override
            public Iterator<Integer> iterator() {
                return new Iterator<Integer>() {
                    @Override
                    public boolean hasNext() {
                        return false;
                    }

                    @Override
                    public Integer next() {
                        return null;
                    }
                };
            }
        };

        // method가 1개이니 lambda로 변경
        Iterable<Integer> iter3 = () -> {
            return new Iterator<Integer>() {
                @Override
                public boolean hasNext() {
                    return false;
                }

                @Override
                public Integer next() {
                    return null;
                }
            };
        };

        Iterable<Integer> iter4 = () -> new Iterator<Integer>() {
            int i = 0;
            final static int MAX = 10;

            @Override
            public boolean hasNext() {
                return i < MAX;
            }

            @Override
            public Integer next() {
                return ++i;
            }
        };

        // Iterable이 구현되어 있으면 for-each 사용 가능
        for (Integer i : iter4) { // for-each
            System.out.println("4-1:" + i);
        }

        for (Iterator<Integer> it = iter4.iterator(); it.hasNext(); ) {
            System.out.println("4-2:" + it.next());
        }
    }

}