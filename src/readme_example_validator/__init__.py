"""Ferramentas para validar exemplos Python marcados em arquivos README."""

from .parser import ExampleBlock, extract_examples
from .runner import ExecutionResult, execute_example

__version__ = "0.1.0"

__all__ = ["ExampleBlock", "ExecutionResult", "execute_example", "extract_examples"]
