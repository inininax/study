package study.jpa.domain;

import lombok.Getter;
import lombok.Setter;

import javax.persistence.Column;
import javax.persistence.MappedSuperclass;
import java.time.LocalDateTime;

@Getter
@Setter
@MappedSuperclass
public class BaseEntity {
    @Column(name = "created_by")
    private long createdBy;

    @Column(name = "created_at")
    private LocalDateTime createdAt;

    @Column(name = "last_modified_by")
    private long lastModifiedBy;

    @Column(name = "last_modified_at")
    private LocalDateTime lastModifiedAt;
}
