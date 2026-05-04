# Projeto Final de Aprendizagem de Maquina, Repositorio-Template (Graduacao)

Estrutura de codigo de referencia para a Etapa 2 do Projeto Final da disciplina de Aprendizagem de Maquina (graduacao). Versao enxuta da derivacao da pos-graduacao, focada em comparacao descritiva. Este template padroniza:

1. Carregamento de 9 datasets do TabArena-v0.1 (3 small + 3 medium + 3 large).
2. Implementacao dos baselines (LightGBM, CatBoost, XGBoost) via `pytabkit`.
3. Pipeline de split (70/30 com seed fixa), tuning com Optuna, avaliacao das metricas exigidas.
4. Analise descritiva: tabela media+/-desvio por modelo, graficos de barras e boxplot, analise por regime.
5. Smoke test que valida os 3 baselines mais o pipeline de plots em um dataset pequeno.

> **Nota.** A versao da pos-graduacao deste mesmo template inclui adicionalmente AutoGluon (default e extreme), modelos foundation que exigem GPU, e analise estatistica rigorosa (Friedman/Nemenyi via `autorank`, Bayesian signed-rank com ROPE via `baycomp`). Aqui na graduacao essas etapas sao omitidas para reduzir a complexidade tecnica e de infraestrutura.

## Status do template

A tabela abaixo indica, para cada componente, o que ja esta implementado e validado e o que cabe a cada grupo preencher. As convencoes sao:

- **Pronto** componente implementado e validado por smoke test; nada a fazer.
- **Esqueleto** ha um arquivo funcional, porem generico, que cada grupo deve adaptar ao seu modelo.
- **Placeholder** ha apenas um stub; o grupo precisa implementar.
- **Acao do aluno** entrega que nao esta no template e o grupo deve produzir do zero.

| Componente | Status | O que falta |
|---|---|---|
| `data/load_tabarena.py`, carregamento via OpenML | Pronto | Substituir `RECOMMENDED_TASK_IDS` (lista provisoria de 9 IDs) pela lista oficial escolhida, validando com `summarize()`. |
| `src/models/baselines.py` (LightGBM, XGBoost, CatBoost via pytabkit) | Pronto | Nada. |
| `src/models/group_model.py` (modelo principal do grupo) | Placeholder | Implementar `build_group_model(seed)` retornando o estimador atribuido (ver exemplos comentados no proprio arquivo). |
| `src/pipeline/split.py` (70/30 estratificado) | Pronto | Nada. |
| `src/pipeline/tune.py` (Optuna, generico) | Esqueleto | Cada grupo define o `search_space` apropriado para o seu modelo. Para baselines `pytabkit` com defaults TD, o tuning pode ser opcional. |
| `src/pipeline/evaluate.py` (AUC OvO, ACC, G-Mean, CE, tempo) | Pronto | Nada. |
| `src/pipeline/regime.py` (quebra por regime) | Pronto | Nada. |
| `src/pipeline/run_all.py` (orquestrador CLI) | Pronto | Cada grupo passa `--include-group-model` apos implementar `group_model.py`. |
| `src/reports/results_table.py` (resumos e exportacao Markdown) | Pronto | Nada. |
| `src/reports/plots.py` (barras, boxplot, regime, time-vs-quality) | Pronto | Nada. |
| `notebooks/01_eda.ipynb` ate `04_analise_resultados.ipynb` | Esqueleto | Executar e adaptar; usar para gerar figuras e tabelas do relatorio. |
| `model_cards/TEMPLATE.md` | Placeholder | Copiar para `model_cards/<seu-modelo>.md` e preencher todos os campos. |
| `tests/test_pipeline.py` (smoke test) | Pronto | Nada. |
| Tabela de selecao dos 9 datasets (no relatorio) | Acao do aluno | Construir tabela com nome, task ID OpenML, n, n_features, n_classes e regime. |
| Relatorio final em PDF | Acao do aluno | Escrever conforme exigencias do projeto. |
| Slides da apresentacao | Acao do aluno | Produzir conforme exigencias do projeto. |

## Modelos atribuiveis aos grupos

| # | Modelo | Toolkit |
|---|---|---|
| 1 | TabM | `pytabkit` |
| 2 | RealMLP | `pytabkit` |
| 3 | FT-Transformer | `pytabkit` |
| 4 | EBM | `interpret` |
| 5 | xRFM | `xrfm` |
| 6 | ModernNCA | `LAMDA-Tabular/TALENT` |
| 7 | Mambular | `deeptab` |

Todos os 7 modelos rodam em laptop comum sem GPU. Modelos foundation (TabPFN, TabICL) e que exigem GPU para uso pratico (Trompt) estao reservados para a versao da pos-graduacao.

## Quickstart

Pre-requisitos: Python 3.11 ou superior e [`uv`](https://docs.astral.sh/uv/) (recomendado) ou `pip`.

```bash
# clonar o repositorio
git clone <url-do-template>
cd projeto-final-AM-grad

# opcao A: uv (recomendado)
uv sync

# opcao B: pip
pip install -e .

# rodar o smoke test (verifica que cada baseline e os plots executam)
pytest tests/test_pipeline.py -v
```

Para rodar o experimento completo com o seu modelo atribuido:

```bash
# editar src/models/group_model.py para apontar para o modelo do grupo
# rodar o pipeline em todos os 9 datasets:
python -m src.pipeline.run_all --include-group-model --seed 42
```

## Estrutura

```
projeto-final-AM-grad/
|- README.md
|- pyproject.toml
|- Dockerfile
|- .python-version
|- data/
|   |- load_tabarena.py
|- src/
|   |- models/
|   |   |- baselines.py
|   |   |- group_model.py
|   |- pipeline/
|       |- split.py
|       |- tune.py
|       |- evaluate.py
|       |- regime.py
|       |- run_all.py
|   |- reports/
|       |- results_table.py
|       |- plots.py
|- notebooks/
|   |- 01_eda.ipynb
|   |- 02_demo_baselines.ipynb
|   |- 03_demo_modelo_grupo.ipynb
|   |- 04_analise_resultados.ipynb
|- model_cards/
|   |- TEMPLATE.md
|- docs/
|   |- INFRAESTRUTURA.md
|- tests/
    |- test_pipeline.py
```

## Fluxo de trabalho recomendado

1. **EDA inicial:** rodar `notebooks/01_eda.ipynb` para inspecionar os 9 datasets.
2. **Baselines:** rodar `notebooks/02_demo_baselines.ipynb` para confirmar que LightGBM, CatBoost e XGBoost executam end-to-end.
3. **Modelo do grupo:** implementar o wrapper em `src/models/group_model.py` e validar em `notebooks/03_demo_modelo_grupo.ipynb`.
4. **Experimento completo:** rodar `python -m src.pipeline.run_all --include-group-model --seed 42`.
5. **Analise descritiva e por regime:** abrir `notebooks/04_analise_resultados.ipynb` e gerar tabela, barras, boxplot e graficos por regime.
6. **Model card:** copiar `model_cards/TEMPLATE.md` para `model_cards/<nome-do-modelo>.md` e preencher.

## Reprodutibilidade

1. Seed fixa em todas as etapas (`split`, `tune`, `evaluate`).
2. Versoes fixadas no `pyproject.toml`.
3. Dockerfile opcional disponivel para containerizacao.
4. Saidas intermediarias (resultados por dataset por modelo) sao gravadas em CSV em `results/`.

## Licencas

Todas as bibliotecas utilizadas tem licencas permissivas (MIT, Apache 2.0). Nenhum dos modelos atribuiveis na versao graduacao requer licenca nao-comercial ou pesos pre-treinados restritos.

## Suporte

Em caso de duvida tecnica, consulte primeiro `docs/INFRAESTRUTURA.md`. Se a duvida persistir, abrir issue no repositorio do template ou contatar o professor da disciplina.
