package study.querydsl.entity;

import lombok.AccessLevel;
import lombok.EqualsAndHashCode;
import lombok.Getter;
import lombok.NoArgsConstructor;

import javax.persistence.*;
import java.time.LocalDateTime;

@Entity
@Getter
@NoArgsConstructor(access = AccessLevel.PROTECTED)
@EqualsAndHashCode
public class Hello extends BaseEntity {
    @Id @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Column(name = "hello_id")
    private Long id;                // hello_id           bigint auto_increment primary key,
    private long id2;               // id2                bigint       not null,
    private String name;            // age                int          null,
    private Integer age;            // age2               int          not null,
    private int age2;               // name               varchar(255) null,
    private Double testDouble;      // test_double        double       null,
    private double testDouble2;     // test_double2       double       not null,
    private Float testFloat;        // test_float         float        null,
    private float testFloat2;       // test_float2        float        not null,
    private char testChar;          // test_char          char         not null,
    private Character testChar2;    // test_char2         char         null,
    private LocalDateTime joinDate; // join_date          datetime(6)  null,
    private Boolean enabled;        // enabled            bit          null,
    private boolean enabled2;       // enabled2           bit          not null,
}
