package jpabook.jpashop.domain.entity.base;

import lombok.Getter;
import lombok.Setter;

import javax.persistence.MappedSuperclass;
import java.time.LocalDateTime;

@MappedSuperclass
@Getter @Setter
public class BaseEntity {
    private Long createdBy;
    private LocalDateTime createdDate;
    private Long lastModifiedBy;
    private LocalDateTime lastModifiedDate;
}