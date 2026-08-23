"""Prompt Engineering demo (stdlib only).

Few-shot 프롬프트 빌더: 템플릿 변수 치환 + 예시(few-shot) 조립 + 간단한 토큰 추정.
"""

SYSTEM_ROLE = "당신은 친근한 영어 선생님입니다."

PROMPT_TEMPLATE = """{role}

다음 규칙에 따라 답변을 작성해 주세요.
- 단순하고 이해하기 쉬운 영어로 설명
- {max_sentences}문장 이내로 작성

예시:
{examples}

Task: {task}
Assistant:"""

FEW_SHOT_EXAMPLES = [
    ("User: 안녕이 뭐야?", "Assistant: Hello는 사람을 만났을 때 인사하는 말이야."),
    ("User: 사과가 뭐야?", "Assistant: Apple은 먹으면 달콤한 과일이야."),
]


def render_template(template: str, **variables: str) -> str:
    """{key} 플레이스홀더를 치환한다. 정의되지 않은 키가 남으면 오류."""
    result = template.format(**variables)
    leftover = _find_placeholders(result)
    if leftover:
        raise ValueError(f"치환되지 않은 플레이스홀더: {leftover}")
    return result


def build_few_shot_prompt(task: str, examples=FEW_SHOT_EXAMPLES, max_sentences: int = 3) -> str:
    rendered = "\n".join(f"{q}\n{a}" for q, a in examples)
    return render_template(
        PROMPT_TEMPLATE,
        role=SYSTEM_ROLE,
        max_sentences=str(max_sentences),
        examples=rendered,
        task=task,
    )


def estimate_tokens(text: str, chars_per_token: float = 3.5) -> int:
    """간이 토큰 추정: 영어 기준 평균 1토큰 ~= 4자, 한글은 글자당 1~2토큰.

    여기서는 문자 수 / chars_per_token 으로 러프하게 추정한다.
    """
    return max(1, round(len(text) / chars_per_token))


def _find_placeholders(text: str) -> list[str]:
    import re

    return re.findall(r"\{[a-zA-Z_][a-zA-Z0-9_]*\}", text)


if __name__ == "__main__":
    prompt = build_few_shot_prompt("나폴레옹이 누구야?")
    print(prompt)
    print("-" * 40)
    print(f"추정 토큰 수: ~{estimate_tokens(prompt)}")
