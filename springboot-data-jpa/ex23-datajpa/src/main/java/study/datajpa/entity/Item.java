package study.datajpa.entity;

import lombok.AccessLevel;
import lombok.NoArgsConstructor;
import org.springframework.data.annotation.CreatedDate;
import org.springframework.data.domain.Persistable;
import org.springframework.data.jpa.domain.support.AuditingEntityListener;

import javax.persistence.Entity;
import javax.persistence.EntityListeners;
import javax.persistence.Id;
import java.time.LocalDateTime;

/**
 * @GeneratedValue를 사용하지 않고 강제로 ID를 세팅하는 경우
 * implements Persistable<ID>를 사용하여 getId(), isNew()를 구현함으로써
 * jpa 내부 로직에서 em.merge가 호출되는 것을 막을 수 있다. (merge는 select를 호출하며 merge 보다는 변경 감지를 사용할 것을 권장)
 */
@Entity
@EntityListeners(AuditingEntityListener.class)
@NoArgsConstructor(access = AccessLevel.PROTECTED)
public class Item implements Persistable<String> {
    @Id
    private String id;

    @CreatedDate
    private LocalDateTime createdDate;

    public Item(String id) {
        this.id = id;
    }

    @Override
    public String getId() {
        return id;
    }

    @Override
    public boolean isNew() {
        return createdDate == null;
    }

    public LocalDateTime getCreatedDate() {
        return createdDate;
    }
}
