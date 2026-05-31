package study.jpa.domain;

import javax.persistence.*;

@Entity
@Table(name = "member_table")
@TableGenerator(
        name = "member_table_seq_generator",
        table = "my_sequences",
        pkColumnValue = "member_table_seq",
        allocationSize = 1
)
public class MemberTable {
    @Id
    @GeneratedValue(strategy = GenerationType.TABLE, generator = "member_table_seq_generator")
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
