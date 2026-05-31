package study.jpa.domain;

import javax.persistence.*;

@Entity
@Table(name = "member_identity")
public class MemberIdentity {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(name = "name", insertable = true, updatable = false, nullable = false, length = 10, columnDefinition = "varchar(100) default 'EMPTY'")
    private String username;

    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public String getUsername() {
        return username;
    }

    public void setUsername(String username) {
        this.username = username;
    }
}
