package jpabook.jpashop.service.simplequery;

import lombok.AllArgsConstructor;
import lombok.Data;

@AllArgsConstructor
@Data
public class Result<T> {
    private T data;
}