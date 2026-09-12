"""Renderização textual e decisão de sucesso agregado."""

from .runner import ExecutionResult

_MAX_OUTPUT = 500


def _summarize(text: str) -> str:
    cleaned = text.strip()
    if len(cleaned) <= _MAX_OUTPUT:
        return cleaned
    return f"{cleaned[:_MAX_OUTPUT]}..."


def is_success(results: list[ExecutionResult]) -> bool:
    """Retorna sucesso somente quando ao menos um exemplo passou."""
    return bool(results) and all(result.status == "passed" for result in results)


def render_report(results: list[ExecutionResult]) -> str:
    """Produz o relatório em português para o terminal."""
    if not results:
        return "Nenhum exemplo marcado foi encontrado. Use a cerca ```python readme-example."

    passed = sum(result.status == "passed" for result in results)
    failed = sum(result.status == "failed" for result in results)
    timed_out = sum(result.status == "timeout" for result in results)
    lines = [
        f"Total de exemplos: {len(results)} | aprovados: {passed} | falhos: {failed} | expirados: {timed_out}"
    ]

    labels = {"passed": "APROVADO", "failed": "FALHOU", "timeout": "EXPIRADO"}
    for result in results:
        lines.append(f"[{labels[result.status]}] linha {result.example.line}")
        if result.status == "failed":
            lines.append(f"  Código de saída: {result.returncode}")
        if result.status != "passed":
            details = _summarize(result.stderr) or _summarize(result.stdout)
            if details:
                lines.append(f"  Saída: {details}")
            elif result.status == "timeout":
                lines.append("  Saída: o exemplo excedeu o tempo limite configurado.")

    return "\n".join(lines)
