# Infraestrutura e ferramentas, guia pratico

Este documento e um tutorial passo-a-passo das ferramentas que o projeto usa. Comece pelo topo se voce nunca configurou um ambiente Python para um projeto cientifico; pule para a secao especifica se voce ja tem o basico.

Sumario:

1. [O que voce precisa instalado na maquina](#1-o-que-voce-precisa-instalado-na-maquina)
2. [Por que ambiente virtual e qual usar](#2-por-que-ambiente-virtual-e-qual-usar)
3. [Caminho A, com `uv` (recomendado)](#3-caminho-a-com-uv-recomendado)
4. [Caminho B, com `pip` e `venv`](#4-caminho-b-com-pip-e-venv)
5. [Caminho C, com `poetry`](#5-caminho-c-com-poetry)
6. [Como o `pyproject.toml` funciona](#6-como-o-pyprojecttoml-funciona)
7. [Rodar o smoke test](#7-rodar-o-smoke-test)
8. [Rodar os notebooks](#8-rodar-os-notebooks)
9. [Containerizar com Docker (opcional)](#9-containerizar-com-docker-opcional)
10. [Reprodutibilidade e seeds](#10-reprodutibilidade-e-seeds)
11. [Troubleshooting comum](#11-troubleshooting-comum)

---

## 1. O que voce precisa instalado na maquina

| Ferramenta | Versao recomendada | Como verificar |
|---|---|---|
| Python | 3.11 ou 3.12 | `python --version` |
| `pip` | qualquer recente | `pip --version` |
| `git` | qualquer recente | `git --version` |
| `uv` (opcional, recomendado) | 0.4 ou superior | `uv --version` |
| Docker (opcional) | 24 ou superior | `docker --version` |

Se Python nao estiver instalado:

- **Windows**: baixar do site oficial (`python.org/downloads`) e marcar a opcao "Add Python to PATH".
- **macOS**: `brew install python@3.11` (Homebrew) ou baixar do site oficial.
- **Linux**: `sudo apt install python3.11 python3.11-venv` (Ubuntu/Debian) ou equivalente.

---

## 2. Por que ambiente virtual e qual usar

Um ambiente virtual e um diretorio isolado com sua propria copia do Python e suas proprias bibliotecas. Sem isolamento, instalar uma versao especifica de `numpy` para este projeto poderia quebrar outro projeto que precisa de versao diferente.

Tres opcoes principais:

- **`uv`** (recomendado): rapido, moderno (2024-2025), gerencia tudo via `pyproject.toml`.
- **`pip` + `venv`**: tradicional, esta em qualquer instalacao Python.
- **`poetry`**: alternativa madura, popular desde 2018.

Os tres caminhos abaixo levam ao mesmo resultado, escolha um.

---

## 3. Caminho A, com `uv` (recomendado)

Instalar o `uv` (uma unica vez):

```bash
# Windows (PowerShell)
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

# macOS / Linux
curl -LsSf https://astral.sh/uv/install.sh | sh
```

No diretorio do template:

```bash
# clonar o template
git clone <url-do-template>
cd projeto-final-AM-grad

# o uv le pyproject.toml, cria .venv e instala tudo:
uv sync

# rodar qualquer comando dentro do ambiente:
uv run pytest tests/test_pipeline.py -v
uv run python -m src.pipeline.run_all --seed 42
uv run jupyter lab
```

O arquivo `uv.lock` e gerado automaticamente, fixando versoes exatas. Comite-o junto com o codigo para garantir reprodutibilidade total.

---

## 4. Caminho B, com `pip` e `venv`

```bash
cd projeto-final-AM-grad

# criar o ambiente virtual
python -m venv .venv

# ativar
# Windows (cmd.exe)
.venv\Scripts\activate
# Windows (PowerShell)
.venv\Scripts\Activate.ps1
# macOS / Linux
source .venv/bin/activate

# instalar o projeto e suas dependencias
pip install --upgrade pip
pip install -e .

# rodar
pytest tests/test_pipeline.py -v
python -m src.pipeline.run_all --seed 42
jupyter lab
```

Para sair do ambiente: `deactivate`.

---

## 5. Caminho C, com `poetry`

Instalar `poetry` (uma unica vez): `pipx install poetry` ou conforme `python-poetry.org`.

```bash
cd projeto-final-AM-grad
poetry install
poetry run pytest tests/test_pipeline.py -v
poetry run python -m src.pipeline.run_all --seed 42
poetry shell  # entra no ambiente
```

Observacao: o `pyproject.toml` deste template segue o padrao PEP 621 (compativel com `uv` e `pip install -e .`). Para usar com `poetry`, talvez seja necessario adaptar a secao `[build-system]`.

---

## 6. Como o `pyproject.toml` funciona

E um arquivo de texto que descreve:

1. **Metadados** do projeto (nome, versao, autores).
2. **Dependencias** obrigatorias (`dependencies`).
3. **Dependencias opcionais** (`[project.optional-dependencies]`), por exemplo um grupo `dev` com `pytest`, `ruff`, `jupyter`.
4. **Versao minima do Python** (`requires-python`).
5. **Configuracao de ferramentas** (pytest, ruff, etc.) na secao `[tool.*]`.

Exemplo simplificado:

```toml
[project]
name = "meu-projeto"
version = "0.1.0"
requires-python = ">=3.11,<3.13"
dependencies = [
    "numpy>=1.26,<3.0",
    "pandas>=2.2,<4.0",
]

[project.optional-dependencies]
dev = ["pytest>=8.0,<10.0"]
```

Os simbolos `>=` e `<` definem ranges de versao compativeis. Ferramentas como `uv`, `pip` e `poetry` resolvem essas restricoes e instalam as versoes adequadas.

---

## 7. Rodar o smoke test

O smoke test (`tests/test_pipeline.py`) valida que cada baseline (LightGBM, XGBoost, CatBoost) executa de ponta a ponta no dataset `breast_cancer`, e que os modulos de plot tambem funcionam. Roda em menos de 90 segundos na primeira vez.

```bash
# com uv
uv run pytest tests/test_pipeline.py -v

# com venv ativo
pytest tests/test_pipeline.py -v
```

Saida esperada: `9 passed`. Se algum teste falhar, normalmente e por dependencia faltando ou versao incompativel; ver secao 11.

---

## 8. Rodar os notebooks

```bash
# com uv
uv run jupyter lab

# com venv ativo
jupyter lab
```

Abra `notebooks/01_eda.ipynb` para EDA inicial. A ordem recomendada: 01 (EDA) -> 02 (baselines) -> 03 (modelo do grupo) -> 04 (analise descritiva e por regime).

---

## 9. Containerizar com Docker (opcional)

Se voce quer rodar o projeto exatamente igual em qualquer maquina (Windows, Linux, servidor), use Docker. Tudo o que precisa ja esta no `Dockerfile`:

```bash
# construir a imagem (uma vez)
docker build -t projeto-final-am-grad .

# rodar o smoke test dentro do container
docker run --rm projeto-final-am-grad

# abrir um shell para usar interativamente
docker run --rm -it -v "$(pwd)":/workspace projeto-final-am-grad bash
```

A imagem fica isolada do seu sistema; voce pode deletar com `docker image rm projeto-final-am-grad` quando nao precisar mais.

---

## 10. Reprodutibilidade e seeds

Reprodutibilidade significa que rodar o mesmo codigo, com os mesmos dados, gera o mesmo resultado. Para isso:

1. **Seed fixa em todos os pontos aleatorios.** O template usa `seed=42` por default em `split`, `tune` e nos modelos.
2. **Versoes fixadas.** O `pyproject.toml` define ranges, e o `uv.lock` (ou `requirements.txt` gerado por `pip freeze`) fixa versoes exatas.
3. **Dados imutaveis.** O OpenML versiona os datasets via `task_id`. Use sempre o mesmo `task_id` para garantir o mesmo dado.
4. **Hash do commit.** Inclua no relatorio o `git rev-parse HEAD` da versao usada nos experimentos.

Cuidado: alguns frameworks introduzem pequenas variacoes mesmo com seed fixa (paralelismo, ordenacao de hash); nesses casos, documente isso como limitacao.

---

## 11. Troubleshooting comum

**`pip install -e .` falha com "Acesso negado".**
- Voce esta tentando instalar no Python global. Crie um `venv` (secao 4) e ative antes de instalar.

**`pytest` reclama de import.**
- Verifique que voce esta no diretorio raiz do projeto (`projeto-final-AM-grad/`) e que o `venv` esta ativo.

**Conflito de versoes entre `numpy` e `pandas` ou `scikit-learn`.**
- Apague `.venv/` e recrie: `rm -rf .venv && uv sync` (ou equivalente em pip). Versoes muito antigas instaladas globalmente podem interferir.

**MiKTeX no Windows nao compila o `.tex` (caso esteja recompilando o documento).**
- Rode `pdflatex` duas vezes para resolver referencias do `hyperref`.
- Se aparecer "running on unsupported version of Windows", e apenas aviso, o PDF e gerado normalmente.

**`uv sync` e muito lento na primeira vez.**
- Normal, a primeira execucao baixa todas as dependencias (centenas de MB). As proximas sao instantaneas pelo cache.

**Treino do modelo do grupo demora muito.**
- Em laptop sem GPU, modelos baseados em redes neurais (TabM, RealMLP, FT-Transformer, Mambular) podem levar varios minutos por dataset. Comece testando em datasets pequenos antes de rodar todos os 9.

---

## Referencias

- Python venv: https://docs.python.org/3/library/venv.html
- pyproject.toml (PEP 621): https://peps.python.org/pep-0621/
- uv: https://docs.astral.sh/uv/
- poetry: https://python-poetry.org/
- Docker: https://docs.docker.com/get-started/
- Optuna: https://optuna.org/
- OpenML: https://www.openml.org/
- Model cards: https://arxiv.org/abs/1810.03993
