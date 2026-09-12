"""Extração de blocos Python explicitamente marcados em Markdown."""

from dataclasses import dataclass

OPENING_FENCE = "```python readme-example"
CLOSING_FENCE = "```"


@dataclass(frozen=True)
class ExampleBlock:
    """Um exemplo extraído, com a linha onde seu código começa."""

    line: int
    content: str


def extract_examples(markdown: str) -> list[ExampleBlock]:
    """Extrai blocos abertos exatamente por `````python readme-example```."""
    examples: list[ExampleBlock] = []
    lines = markdown.splitlines(keepends=True)
    index = 0

    while index < len(lines):
        if lines[index].strip() != OPENING_FENCE:
            index += 1
            continue

        code_start = index + 1
        index += 1
        content: list[str] = []
        while index < len(lines) and lines[index].strip() != CLOSING_FENCE:
            content.append(lines[index])
            index += 1

        if index < len(lines):
            examples.append(ExampleBlock(line=code_start + 1, content="".join(content)))
            index += 1

    return examples
