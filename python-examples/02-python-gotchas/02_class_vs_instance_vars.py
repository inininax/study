"""
02_class_vs_instance_vars.py - 🔴 클래스 변수 vs 인스턴스 변수 혼동

📌 핵심 개념:
    Python의 클래스 변수는 모든 인스턴스가 공유합니다.
    가변 객체를 클래스 변수로 선언하면 예기치 않은 공유가 발생합니다.

🔄 다른 언어 비교:
    - Java: 인스턴스 변수와 static 변수가 명확히 구분됨
    - Go: 구조체에 static 개념 없음
    - Kotlin: 클래스 필드와 companion object 분리
    - Python: 클래스 body에 선언하면 클래스 변수 (공유됨!)

⚠️ 주의사항:
    Java의 인스턴스 변수처럼 보이지만, Python은 다르게 동작합니다!

📚 참고: https://docs.python.org/3/tutorial/classes.html#class-and-instance-variables
"""

from __future__ import annotations


# =============================================================================
# 1️⃣ ❌ 잘못된 패턴 - 클래스 변수로 가변 객체 선언
# =============================================================================

def wrong_class_variable_demo() -> None:
    """
    ❌ 잘못된 패턴: 가변 객체를 클래스 변수로 선언.
    
    💡 Java 개발자를 위한 팁:
        Java에서 이렇게 작성하면 인스턴스 변수입니다:
        
        Java:
            class User {
                List<String> items = new ArrayList<>();  // 인스턴스 변수
            }
            
        하지만 Python에서는 클래스 변수입니다:
        
        Python:
            class User:
                items = []  # 클래스 변수! 모든 인스턴스가 공유!
    """
    # ❌ 잘못된 클래스 정의
    class WrongUser:
        # 클래스 변수 - 모든 인스턴스가 공유!
        tags: list[str] = []
        
        def __init__(self, name: str) -> None:
            self.name = name
        
        def add_tag(self, tag: str) -> None:
            self.tags.append(tag)
    
    print("❌ 클래스 변수 공유 문제:")
    user1 = WrongUser("Alice")
    user1.add_tag("admin")
    print(f"  user1.tags: {user1.tags}")
    
    user2 = WrongUser("Bob")
    print(f"  user2.tags (새 객체!): {user2.tags}")  # ['admin'] 이미 있음!
    
    user2.add_tag("member")
    print(f"  user1.tags: {user1.tags}")  # ['admin', 'member']
    print(f"  user2.tags: {user2.tags}")  # 같은 리스트!
    
    print(f"\n  user1.tags is user2.tags: {user1.tags is user2.tags}")  # True!
    print(f"  WrongUser.tags: {WrongUser.tags}")  # 클래스 변수로 접근


# =============================================================================
# 2️⃣ ✅ 올바른 패턴 - __init__에서 인스턴스 변수 초기화
# =============================================================================

def correct_instance_variable_demo() -> None:
    """
    ✅ 올바른 패턴: __init__에서 인스턴스 변수를 초기화.
    """
    # ✅ 올바른 클래스 정의
    class CorrectUser:
        def __init__(self, name: str) -> None:
            self.name = name
            self.tags: list[str] = []  # 인스턴스 변수 - 각 인스턴스마다 독립!
        
        def add_tag(self, tag: str) -> None:
            self.tags.append(tag)
    
    print("✅ 인스턴스 변수 사용:")
    user1 = CorrectUser("Alice")
    user1.add_tag("admin")
    print(f"  user1.tags: {user1.tags}")
    
    user2 = CorrectUser("Bob")
    print(f"  user2.tags (새 객체): {user2.tags}")  # [] - 독립적!
    
    user2.add_tag("member")
    print(f"  user1.tags: {user1.tags}")  # ['admin'] - 변경 없음
    print(f"  user2.tags: {user2.tags}")  # ['member']
    
    print(f"\n  user1.tags is user2.tags: {user1.tags is user2.tags}")  # False!


# =============================================================================
# 3️⃣ 클래스 변수의 올바른 사용
# =============================================================================

def proper_class_variable_demo() -> None:
    """
    클래스 변수의 올바른 사용 예시.
    """
    class Counter:
        # ✅ 클래스 변수의 올바른 사용 - 모든 인스턴스에서 공유해야 할 때
        instance_count: int = 0
        
        def __init__(self, name: str) -> None:
            self.name = name
            Counter.instance_count += 1  # 클래스 변수 수정
        
        @classmethod
        def get_count(cls) -> int:
            return cls.instance_count
    
    print("✅ 클래스 변수 올바른 사용:")
    print(f"  초기 카운트: {Counter.instance_count}")
    
    c1 = Counter("First")
    c2 = Counter("Second")
    c3 = Counter("Third")
    
    print(f"  3개 생성 후: {Counter.instance_count}")
    print(f"  c1.instance_count: {c1.instance_count}")  # 클래스 변수 접근 가능
    
    # 상수로 클래스 변수 사용
    class Config:
        MAX_CONNECTIONS: int = 100
        DEFAULT_TIMEOUT: float = 30.0
        API_VERSION: str = "v1"
    
    print(f"\n  Config.MAX_CONNECTIONS: {Config.MAX_CONNECTIONS}")


# =============================================================================
# 4️⃣ 변수 가리기 (Variable Shadowing)
# =============================================================================

def variable_shadowing_demo() -> None:
    """
    클래스 변수와 인스턴스 변수 가리기.
    """
    class Example:
        class_var: str = "class"
        
        def __init__(self) -> None:
            pass
    
    print("변수 가리기 (Shadowing):")
    
    obj = Example()
    print(f"  obj.class_var: {obj.class_var}")  # 'class' (클래스 변수)
    
    # 인스턴스에 같은 이름으로 할당하면 인스턴스 변수가 됨
    obj.class_var = "instance"
    print(f"  obj.class_var (할당 후): {obj.class_var}")  # 'instance' (인스턴스 변수)
    print(f"  Example.class_var: {Example.class_var}")  # 'class' (클래스 변수는 그대로)
    
    # 새 객체는 여전히 클래스 변수 참조
    obj2 = Example()
    print(f"  obj2.class_var: {obj2.class_var}")  # 'class'
    
    # ⚠️ 하지만 가변 객체에서는 다르게 동작!
    print("\n⚠️ 가변 객체 주의:")
    
    class MutableExample:
        shared_list: list[str] = []
    
    m1 = MutableExample()
    m1.shared_list.append("from m1")  # 클래스 변수 직접 수정!
    
    m2 = MutableExample()
    print(f"  m2.shared_list: {m2.shared_list}")  # ['from m1'] - 공유됨!
    
    # 할당하면 인스턴스 변수로 가려짐
    m1.shared_list = ["new list"]  # 인스턴스 변수 생성
    print(f"  m1.shared_list (할당 후): {m1.shared_list}")
    print(f"  m2.shared_list: {m2.shared_list}")  # 클래스 변수


# =============================================================================
# 5️⃣ dataclass와 클래스 변수
# =============================================================================

def dataclass_demo() -> None:
    """
    dataclass에서의 클래스 변수와 인스턴스 변수.
    """
    from dataclasses import dataclass, field
    
    # ❌ 잘못된 dataclass (하지만 dataclass는 자동으로 처리!)
    @dataclass
    class WrongDataclass:
        name: str
        items: list[str] = field(default_factory=list)  # ✅ factory 사용
    
    print("dataclass의 default_factory:")
    d1 = WrongDataclass("Alice")
    d1.items.append("item1")
    
    d2 = WrongDataclass("Bob")
    print(f"  d1.items: {d1.items}")
    print(f"  d2.items: {d2.items}")  # [] - 독립적!
    
    # 클래스 변수는 ClassVar로 명시
    from typing import ClassVar
    
    @dataclass
    class ConfigurableUser:
        name: str
        email: str = ""
        
        # ClassVar - 명시적으로 클래스 변수
        default_role: ClassVar[str] = "user"
        instance_count: ClassVar[int] = 0
        
        def __post_init__(self) -> None:
            ConfigurableUser.instance_count += 1
    
    print("\n  ClassVar 사용:")
    u1 = ConfigurableUser("Kim")
    u2 = ConfigurableUser("Lee")
    print(f"  instance_count: {ConfigurableUser.instance_count}")


# =============================================================================
# 6️⃣ 요약
# =============================================================================

def summary() -> None:
    """
    클래스 변수 vs 인스턴스 변수 요약.
    """
    print("""
    ╔═══════════════════════════════════════════════════════════════╗
    ║            🔴 클래스 변수 vs 인스턴스 변수 규칙                ║
    ╠═══════════════════════════════════════════════════════════════╣
    ║                                                               ║
    ║  Python의 변수 위치:                                          ║
    ║                                                               ║
    ║    class MyClass:                                             ║
    ║        class_var = []      # ← 클래스 변수 (모든 인스턴스 공유)║
    ║                                                               ║
    ║        def __init__(self):                                    ║
    ║            self.instance_var = []  # ← 인스턴스 변수 (독립적) ║
    ║                                                               ║
    ║  ❌ 하지 마세요:                                               ║
    ║     class User:                                               ║
    ║         items = []  # 모든 인스턴스가 공유!                   ║
    ║                                                               ║
    ║  ✅ 이렇게 하세요:                                             ║
    ║     class User:                                               ║
    ║         def __init__(self):                                   ║
    ║             self.items = []  # 각 인스턴스별 독립             ║
    ║                                                               ║
    ║  💡 클래스 변수가 적절한 경우:                                 ║
    ║     - 상수 (MAX_SIZE, DEFAULT_VALUE)                          ║
    ║     - 인스턴스 카운터                                         ║
    ║     - 모든 인스턴스가 공유해야 하는 설정                      ║
    ║                                                               ║
    ╚═══════════════════════════════════════════════════════════════╝
    """)


# =============================================================================
# 메인 실행
# =============================================================================

def main() -> None:
    """예제 실행."""
    demos = [
        ("1️⃣ ❌ 잘못된 패턴", wrong_class_variable_demo),
        ("2️⃣ ✅ 올바른 패턴", correct_instance_variable_demo),
        ("3️⃣ 클래스 변수 올바른 사용", proper_class_variable_demo),
        ("4️⃣ 변수 가리기", variable_shadowing_demo),
        ("5️⃣ dataclass", dataclass_demo),
        ("6️⃣ 요약", summary),
    ]
    
    print("=" * 60)
    print("🔴 클래스 변수 vs 인스턴스 변수")
    print("=" * 60)
    print()
    
    for title, demo_func in demos:
        print("-" * 60)
        print(f"📌 {title}")
        print("-" * 60)
        demo_func()
        print()


if __name__ == "__main__":
    main()

