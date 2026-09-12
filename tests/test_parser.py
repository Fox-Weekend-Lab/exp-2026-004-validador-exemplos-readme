from readme_example_validator.parser import extract_examples


def test_extracts_marked_examples_and_start_lines():
    markdown = "# Guia\n\n```python readme-example\nprint('one')\n```\nTexto\n```python readme-example\nprint('two')\n```\n"

    examples = extract_examples(markdown)

    assert [example.line for example in examples] == [4, 8]
    assert [example.content for example in examples] == ["print('one')\n", "print('two')\n"]


def test_ignores_unmarked_and_other_language_blocks():
    markdown = "```python\nprint('ignored')\n```\n```bash readme-example\necho ignored\n```\n"

    assert extract_examples(markdown) == []


def test_ignores_unclosed_marked_block():
    markdown = "```python readme-example\nprint('incomplete')\n"

    assert extract_examples(markdown) == []
