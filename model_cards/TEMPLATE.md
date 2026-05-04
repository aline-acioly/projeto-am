# Model Card: <Nome do Modelo>

> Preencha este template com base no modelo principal atribuido ao seu grupo. Substitua os campos `<...>` pelos valores reais. Nao deixe campos em branco; use "N/A" quando nao aplicavel.

## 1. Detalhes do modelo

- **Nome:** <ex.: TabM>
- **Versao:** <ex.: 1.0>
- **Autores originais:** <ex.: Gorishniy et al., 2025>
- **Repositorio oficial:** <URL>
- **Licenca do codigo:** <ex.: Apache 2.0>
- **Familia arquitetural:** <ex.: ensemble parameter-efficient de MLPs>
- **Hiperparametros principais:** <listar; indicar se foi feita busca via Optuna>

## 2. Uso pretendido

- **Caso de uso primario:** classificacao supervisionada em dados tabulares.
- **Casos de uso fora de escopo:** <ex.: dados nao-IID, series temporais, dados de imagem>
- **Usuarios pretendidos:** <ex.: pesquisadores e praticantes de ML em problemas tabulares>

## 3. Dados de treino e avaliacao

- **Origem dos dados (treino):** <ex.: pesos inicializados aleatoriamente; treino direto nos dados do projeto>
- **Origem dos dados (avaliacao neste projeto):** 9 datasets do TabArena-v0.1 (3 small + 3 medium + 3 large).
- **Estrategia de split:** 70/30 estratificado por classe, seed=<n>.
- **Pre-processamento:** <descrever>

## 4. Metricas alcancadas

| Metrica | Media (9 datasets) | Desvio |
|---|---|---|
| AUC OVO | <0.0000> | <0.0000> |
| Accuracy | <0.0000> | <0.0000> |
| G-Mean | <0.0000> | <0.0000> |
| Cross-Entropy | <0.0000> | <0.0000> |
| Tempo total (s) | <0.0> | <0.0> |

### Resultados por regime

- **Tamanho do dataset:** <pequeno: AUC=...; medio: AUC=...; grande: AUC=...>
- **Numero de classes:** <binario: AUC=...; multiclasse: AUC=...>
- **Proporcao categorica:** <baixa: AUC=...; alta: AUC=...>
- **Missing values:** <com NaN: AUC=...; sem NaN: AUC=...>

## 5. Limitacoes conhecidas

- <ex.: tempo de treino cresce linearmente com n e quadraticamente com p>
- <ex.: requer pelo menos 8 GB de RAM para datasets medios>
- <ex.: nao funciona bem em dados altamente desbalanceados sem rebalanceamento>

## 6. Consideracoes eticas

- **Riscos de uso indevido:** <ex.: vies herdado dos dados de treino, decisoes opacas em dominios sensiveis>
- **Impacto ambiental:** <energia consumida durante tuning; latencia de inferencia>
- **Recomendacoes de auditoria:** <ex.: comparar predicoes com baseline interpretavel como EBM antes de deploy>

## 7. Reprodutibilidade

- **Ambiente:** Python <3.11>, dependencias fixadas em `pyproject.toml`.
- **Hardware utilizado:** <CPU, RAM, tempo total de execucao>
- **Comandos para reproduzir:**
  ```bash
  uv sync
  python -m src.pipeline.run_all --include-group-model --seed 42
  ```
- **Hash do commit:** <git rev-parse HEAD>

## 8. Referencias

- <citacao do paper original do modelo>
- TabArena-v0.1 (NeurIPS 2025): https://tabarena.ai
