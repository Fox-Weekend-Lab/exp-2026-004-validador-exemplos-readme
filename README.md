# Validador de Exemplos de README

> Este projeto foi gerado automaticamente por IA e revisado por um agente automatizado, nao por uma pessoa. Leia o codigo antes de usar.

## Descrição

Ferramenta de linha de comando para extrair blocos Python marcados em um arquivo Markdown, executá-los individualmente em diretórios temporários e apresentar um relatório textual de aprovação, falha ou expiração por tempo limite.

O marcador reconhecido é:

````markdown
```python readme-example
print("Olá")
```
````

## Objetivo

Oferecer uma verificação reproduzível para exemplos Python selecionados em um README, identificando a linha de origem de cada exemplo e indicando se sua execução foi concluída com sucesso.

## Como funciona

1. A CLI lê o arquivo README informado.
2. O parser localiza blocos cuja linha de abertura, após remoção de espaços nas extremidades, seja ` ```python readme-example`.
3. Cada bloco fechado por uma linha ` ``` ` é registrado com a linha em que seu código começa.
4. Cada exemplo é gravado como `example.py` em um diretório temporário próprio.
5. O exemplo é executado com o interpretador Python atual, com diretório de trabalho temporário, saídas capturadas e tempo limite configurável.
6. O relatório informa totais e o status de cada exemplo:
   - **APROVADO**: o processo terminou com código de saída `0`;
   - **FALHOU**: o processo terminou com código de saída diferente de `0`;
   - **EXPIRADO**: o processo excedeu o tempo limite.

A execução geral retorna sucesso apenas quando há pelo menos um exemplo marcado e todos os exemplos são aprovados.

## Arquitetura

- `sitecustomize.py`: adiciona o diretório `src/` ao caminho de módulos quando carregado na execução local.
- `requirements.txt`: arquivo de dependências do projeto.
- `src/readme_example_validator/__init__.py`: expõe os modelos e funções principais do pacote e define a versão `0.1.0`.
- `src/readme_example_validator/__main__.py`: implementa a interface de linha de comando, leitura do arquivo e coordenação da validação.
- `src/readme_example_validator/parser.py`: define `ExampleBlock` e extrai blocos Markdown marcados.
- `src/readme_example_validator/runner.py`: define `ExecutionResult` e executa os exemplos em `TemporaryDirectory` com `subprocess.run`.
- `src/readme_example_validator/report.py`: agrega os resultados e renderiza o relatório em português.
- `tests/conftest.py`: suporte compartilhado para os testes.
- `tests/test_cli.py`: testes do fluxo da interface de linha de comando.
- `tests/test_parser.py`: testes da extração de blocos Markdown.
- `tests/test_runner.py`: testes de execução aprovada, falha e tempo limite.

## Tecnologias

- Python 3.11+
- Biblioteca padrão do Python:
  - `argparse`
  - `dataclasses`
  - `pathlib`
  - `subprocess`
  - `tempfile`
  - `os`
  - `sys`
- Markdown, como formato de entrada analisado pelas regras implementadas no parser.
- `pytest`, utilizado para executar a suíte de testes.

## Instalacao

Instale as dependências listadas no arquivo `requirements.txt`:

```bash
python -m pip install -r requirements.txt
```

O projeto usa o layout `src/` e não possui arquivo de instalação do pacote. Por isso, para executar o módulo, `src/` precisa estar no `PYTHONPATH`.

## Configuracao

A ferramenta não lê variáveis de ambiente específicas para configuração.

O tempo limite por exemplo é configurado pela opção `--timeout` da CLI. O valor padrão é `5.0` segundos e o valor informado deve ser maior que zero.

Durante a execução dos exemplos, o processo filho recebe uma cópia das variáveis de ambiente do processo que iniciou o validador.

## Uso

Informe o caminho do README a validar como argumento posicional.

Linux/macOS:

```bash
PYTHONPATH=src python -m readme_example_validator README.md
```

Windows (PowerShell):

```powershell
$env:PYTHONPATH="src"; python -m readme_example_validator README.md
```

Para definir outro tempo limite, use `--timeout` em segundos:

Linux/macOS:

```bash
PYTHONPATH=src python -m readme_example_validator README.md --timeout 10
```

Windows (PowerShell):

```powershell
$env:PYTHONPATH="src"; python -m readme_example_validator README.md --timeout 10
```

Se o caminho não apontar para um arquivo existente, se o arquivo não puder ser lido ou se não estiver em UTF-8, a CLI exibe uma mensagem de erro e retorna código `2`. Quando houver exemplos falhos, expirados ou nenhum exemplo marcado, retorna código `1`.

## Exemplos

Um README pode conter exemplos como o seguinte:

````markdown
# Meu projeto

```python readme-example
print("Exemplo válido")
```
````

Blocos Python sem o marcador não são executados:

````markdown
```python
print("Este bloco é ignorado")
```
````

Um relatório com um exemplo bem-sucedido tem o formato:

```text
Total de exemplos: 1 | aprovados: 1 | falhos: 0 | expirados: 0
[APROVADO] linha 4
```

Em caso de falha, o relatório inclui o código de saída e, quando disponível, uma saída capturada. As saídas exibidas são resumidas para manter o terminal legível.

## Testes

Execute a suíte com:

```bash
python -m pytest
```

Os testes não acessam a rede. Eles utilizam apenas código Python local e determinístico em arquivos e processos temporários.

## Limitacoes

- Apenas blocos abertos com o marcador ` ```python readme-example` são considerados; blocos Python comuns e outras linguagens são ignorados.
- Um bloco aberto sem uma cerca de fechamento ` ``` ` não é incluído nos exemplos extraídos.
- A ferramenta executa somente código Python; não executa comandos de shell ou outros formatos de exemplo.
- Os exemplos são executados como processos Python locais. O diretório temporário isola os arquivos criados nele, mas não constitui uma sandbox de segurança.
- O processo executado recebe uma cópia do ambiente do processo chamador.
- A ferramenta não instala dependências, não cria ambiente virtual e não infere dependências necessárias aos exemplos.
- O relatório é textual no terminal; não há saída estruturada, edição automática do README ou integração de CI implementada.
- O relatório resume saídas extensas antes de exibi-las.

## O que foi aprendido

O experimento demonstra uma forma simples de tornar exemplos de documentação verificáveis: usar uma marcação explícita em Markdown, associar cada bloco à sua linha de origem e executar cada trecho separadamente com captura de resultado. Também demonstra o uso de diretórios temporários e de limites de tempo para reduzir resíduos entre execuções e evitar que um exemplo bloqueie indefinidamente a validação.

## Possivel aplicacao na FOX

Pode ser utilizado para validar exemplos Python explicitamente selecionados em READMEs de repositórios e experimentos da FOX antes de revisões ou entregas, apontando trechos que falharam, expiraram ou deixaram de estar presentes.

## Status

O relatório de testes recebido informa que a suíte passou: **9 testes foram coletados e os 9 passaram**.
