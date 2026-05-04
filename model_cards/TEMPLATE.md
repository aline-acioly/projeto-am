# Model Card: <Nome do Modelo>

> Preencha este template com base no modelo principal atribuído ao seu grupo. Substitua os campos `<...>` pelos valores reais. Não deixe campos em branco; use "N/A" quando não aplicável.

## 1. Detalhes do modelo

- **Nome:** <ex.: TabM>
- **Versão:** <ex.: 1.0>
- **Autores originais:** <ex.: Gorishniy et al., 2025>
- **Repositório oficial:** <URL>
- **Licença do código:** <ex.: Apache 2.0>
- **Família arquitetural:** <ex.: ensemble parameter-efficient de MLPs>
- **Hiperparâmetros principais:** <listar; indicar se foi feita busca via Optuna>

## 2. Uso pretendido

- **Caso de uso primário:** classificação supervisionada em dados tabulares.
- **Casos de uso fora de escopo:** <ex.: dados não-IID, séries temporais, dados de imagem>
- **Usuários pretendidos:** <ex.: pesquisadores e praticantes de ML em problemas tabulares>

## 3. Dados de treino e avaliação

- **Origem dos dados (treino):** <ex.: pesos inicializados aleatoriamente; treino direto nos dados do projeto>
- **Origem dos dados (avaliação neste projeto):** 9 datasets do TabArena-v0.1 (3 small + 3 medium + 3 large).
- **Estratégia de split:** 70/30 estratificado por classe, seed=<n>.
- **Pré-processamento:** <descrever>

## 4. Métricas alcançadas

| Métrica | Média (9 datasets) | Desvio |
|---|---|---|
| AUC OVO | <0.0000> | <0.0000> |
| Accuracy | <0.0000> | <0.0000> |
| G-Mean | <0.0000> | <0.0000> |
| Cross-Entropy | <0.0000> | <0.0000> |
| Tempo total (s) | <0.0> | <0.0> |

### Resultados por regime

- **Tamanho do dataset:** <pequeno: AUC=...; médio: AUC=...; grande: AUC=...>
- **Número de classes:** <binário: AUC=...; multiclasse: AUC=...>
- **Proporção categórica:** <baixa: AUC=...; alta: AUC=...>
- **Missing values:** <com NaN: AUC=...; sem NaN: AUC=...>

## 5. Limitações conhecidas

- <ex.: tempo de treino cresce linearmente com n e quadraticamente com p>
- <ex.: requer pelo menos 8 GB de RAM para datasets médios>
- <ex.: não funciona bem em dados altamente desbalanceados sem rebalanceamento>

## 6. Considerações éticas

- **Riscos de uso indevido:** <ex.: viés herdado dos dados de treino, decisões opacas em domínios sensíveis>
- **Impacto ambiental:** <energia consumida durante tuning; latência de inferência>
- **Recomendações de auditoria:** <ex.: comparar predições com baseline interpretável como EBM antes de deploy>

## 7. Reprodutibilidade

- **Ambiente:** Python <3.11>, dependências fixadas em `pyproject.toml`.
- **Hardware utilizado:** <CPU, RAM, tempo total de execução>
- **Comandos para reproduzir:**
  ```bash
  uv sync
  python -m src.pipeline.run_all --include-group-model --seed 42
  ```
- **Hash do commit:** <git rev-parse HEAD>

## 8. Referências

- <citação do paper original do modelo>
- TabArena-v0.1 (NeurIPS 2025): https://tabarena.ai
