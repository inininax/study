package study.jpa.domain;

import javax.persistence.*;

@Entity
@Table(name = "member_sequence")
@SequenceGenerator(
        name = "member_sequence_seq_generator",
        sequenceName = "member_sequence_seq",
        initialValue = 1,
        allocationSize = 1
)
public class MemberSequence {
    @Id
    @GeneratedValue(strategy = GenerationType.SEQUENCE, generator = "member_sequence_seq_generator")
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
