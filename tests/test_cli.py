from readme_example_validator.__main__ import main


def test_cli_reports_success_for_valid_readme(tmp_path, capsys):
    readme = tmp_path / "README.md"
    readme.write_text("```python readme-example\nprint('valid')\n```\n", encoding="utf-8")

    code = main([str(readme), "--timeout", "1"])

    output = capsys.readouterr().out
    assert code == 0
    assert "[APROVADO] linha 2" in output


def test_cli_reports_failure_for_no_examples(tmp_path, capsys):
    readme = tmp_path / "README.md"
    readme.write_text("# Sem exemplos\n", encoding="utf-8")

    code = main([str(readme)])

    assert code == 1
    assert "Nenhum exemplo marcado" in capsys.readouterr().out


def test_cli_rejects_missing_file(capsys):
    code = main(["arquivo-inexistente.md"])

    assert code == 2
    assert "arquivo README existente" in capsys.readouterr().err
