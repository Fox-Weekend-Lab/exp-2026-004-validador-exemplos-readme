from readme_example_validator.parser import ExampleBlock
from readme_example_validator.runner import execute_example


def test_executes_successful_example():
    result = execute_example(ExampleBlock(line=3, content="print('ok')\n"), timeout=1)

    assert result.status == "passed"
    assert result.returncode == 0
    assert result.stdout == "ok\n"


def test_captures_failing_example():
    result = execute_example(ExampleBlock(line=7, content="raise ValueError('bad')\n"), timeout=1)

    assert result.status == "failed"
    assert result.returncode != 0
    assert "ValueError: bad" in result.stderr


def test_marks_example_that_exceeds_timeout():
    code = "import time\ntime.sleep(0.2)\n"
    result = execute_example(ExampleBlock(line=2, content=code), timeout=0.01)

    assert result.status == "timeout"
    assert result.returncode is None
