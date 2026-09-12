"""Execução isolada de exemplos extraídos."""

from dataclasses import dataclass
import os
from pathlib import Path
import subprocess
import sys
from tempfile import TemporaryDirectory

from .parser import ExampleBlock


@dataclass(frozen=True)
class ExecutionResult:
    """Resultado da execução de um exemplo."""

    example: ExampleBlock
    status: str
    returncode: int | None
    stdout: str
    stderr: str


def _text(value: str | bytes | None) -> str:
    if value is None:
        return ""
    if isinstance(value, bytes):
        return value.decode("utf-8", errors="replace")
    return value


def execute_example(example: ExampleBlock, timeout: float) -> ExecutionResult:
    """Executa um exemplo em diretório temporário e captura suas saídas."""
    with TemporaryDirectory(prefix="readme-example-") as directory:
        script = Path(directory) / "example.py"
        script.write_text(example.content, encoding="utf-8")
        try:
            completed = subprocess.run(
                [sys.executable, str(script)],
                cwd=directory,
                env=os.environ.copy(),
                capture_output=True,
                text=True,
                timeout=timeout,
                check=False,
            )
        except subprocess.TimeoutExpired as error:
            return ExecutionResult(
                example=example,
                status="timeout",
                returncode=None,
                stdout=_text(error.stdout),
                stderr=_text(error.stderr),
            )

    status = "passed" if completed.returncode == 0 else "failed"
    return ExecutionResult(
        example=example,
        status=status,
        returncode=completed.returncode,
        stdout=completed.stdout,
        stderr=completed.stderr,
    )
