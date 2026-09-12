"""Interface de linha de comando do validador."""

import argparse
from pathlib import Path
import sys

from .parser import extract_examples
from .report import is_success, render_report
from .runner import execute_example


def _positive_timeout(value: str) -> float:
    try:
        timeout = float(value)
    except ValueError as error:
        raise argparse.ArgumentTypeError("Informe --timeout como um número em segundos.") from error
    if timeout <= 0:
        raise argparse.ArgumentTypeError("Informe --timeout com valor maior que zero.")
    return timeout


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Valida blocos ```python readme-example de um README."
    )
    parser.add_argument("readme", help="Caminho do arquivo README a validar.")
    parser.add_argument(
        "--timeout",
        type=_positive_timeout,
        default=5.0,
        metavar="SEGUNDOS",
        help="Tempo limite por exemplo em segundos (padrão: 5).",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    readme_path = Path(args.readme)
    if not readme_path.is_file():
        print("Erro: informe o caminho de um arquivo README existente.", file=sys.stderr)
        return 2

    try:
        markdown = readme_path.read_text(encoding="utf-8")
    except OSError as error:
        print(f"Erro ao ler o README: {error}. Verifique as permissões do arquivo.", file=sys.stderr)
        return 2
    except UnicodeDecodeError:
        print("Erro: o README deve estar codificado em UTF-8.", file=sys.stderr)
        return 2

    examples = extract_examples(markdown)
    results = [execute_example(example, args.timeout) for example in examples]
    print(render_report(results))
    return 0 if is_success(results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
