# Model Card: TabM

> Estrutura inspirada em Mitchell et al. (2019), com extensões específicas da disciplina.

---

## 1. Detalhes do modelo

- **Nome:** TabM
- **Versão:** 1.0 (ICLR 2025)
- **Autores originais:** Gorishniy et al., Yandex Research, 2025
- **Repositório oficial:** https://github.com/yandex-research/tabm
- **Licença do código:** Apache 2.0
- **Família arquitetural:** Ensemble parameter-efficient de MLPs com k=32 cabeças implícitas e pesos compartilhados (BatchEnsemble)
- **Complexidade computacional:** O(n · p · k) em treino, onde k=32 cabeças; inferência O(p · k) por amostra
- **Toolkit / dependências:** pytabkit 1.7.3, torch 2.7.1, scikit-learn 1.8.0
- **Hiperparâmetros principais:** `k` (número de membros, padrão 32), `lr` ∈ [1e-4, 1e-2], `weight_decay`, `hidden_sizes`, `dropout` — defaults TD usados neste projeto

---

## 2. Uso pretendido

- **Caso de uso primário:** Classificação supervisionada em dados tabulares IID, binários e multiclasse
- **Casos de uso fora de escopo:** Dados não-IID, séries temporais, dados de imagem, texto ou áudio
- **Usuários pretendidos:** Pesquisadores e praticantes em problemas tabulares com benchmarks padronizados
- **Faixa de n suportada:** 1.000–500.000 amostras; GPU recomendada para n > 20.000
- **Condições operacionais:** CPU (8 GB RAM) para datasets pequenos e médios; GPU para large

---

## 3. Fatores observados

- **Tamanho do dataset (n):**
  - **Small (n < 1k):** AUC médio = 0.8721 — melhor desempenho entre todos os modelos neste regime, surpreendendo a expectativa inicial. O ensemble implícito reduz variância mesmo com poucos dados.
  - **Medium (1k–10k):** AUC médio = 0.8193 — margem pequena vs. baselines (CatBoost 0.8198, LightGBM 0.8124). Competitivo.
  - **Large (> 10k):** AUC médio = 0.9275 — levemente superior à média dos GBDTs. Custo computacional alto (>900 s/dataset) é o gargalo.
- **Número de classes:**
  - **Binário:** AUC = 0.8622 — competitivo com baselines.
  - **Multiclasse:** AUC = 0.8945 — vantagem clara do TabM (+0.06 vs. LightGBM). O ensemble implícito ajuda em problemas com múltiplas classes.
- **Proporção entre features categóricas e numéricas:**
  - **Alta proporção categórica (≥ 25%):** AUC = 0.8587 — levemente inferior ao regime de features numéricas. Embeddings ganham menos quando features já são categóricas.
  - **Baixa proporção categórica (< 25%):** AUC = 0.8908 — melhor regime para o TabM; embeddings numéricos periódicos aportam maior ganho.
- **Presença de valores ausentes:**
  - **Com missing (adult):** AUC = 0.9148 — abaixo da média dos GBDTs neste dataset (CatBoost 0.9285, LightGBM 0.9274). Imputação automática nem sempre é suficiente para compensar.
  - **Sem missing:** AUC = 0.8677 — acima dos baselines.

---

## 4. Métricas alcançadas

Tabela agregada nos 9 datasets do TabArena-v0.1. IC 95% via bootstrap (1.000 reamostragens, seed=42).

| Métrica         | Média  | Desvio | IC 95% (bootstrap)   |
| --------------- | ------ | ------ | -------------------- |
| AUC OvO         | 0,8730 | 0,0875 | [0,8165; 0,9325]     |
| Accuracy        | 0,8164 | 0,1121 | [0,7399; 0,8823]     |
| G-Mean          | 0,6942 | 0,1138 | [0,6220; 0,7708]     |
| Cross-Entropy   | 0,4000 | 0,2158 | [0,2697; 0,5601]     |
| Tempo total (s) | 642,7  | 1047,5 | [124,5; 1399,9]      |

### Resultados por regime

- **Tamanho:** small: AUC=0,8721; medium: AUC=0,8193; large: AUC=0,9275
- **Número de classes:** binário: AUC=0,8622; multiclasse: AUC=0,8945
- **Proporção categórica:** baixa (< 25%): AUC=0,8908; alta (≥ 25%): AUC=0,8587
- **Missing values:** com NaN (adult): AUC=0,9148; sem NaN (demais): AUC=0,8677

---

## 5. Dados de avaliação

- **Origem:** 9 datasets do TabArena-v0.1 (NeurIPS 2025), carregados via OpenML
- **Distribuição por regime:** 3 pequenos + 3 médios + 3 grandes
- **Estratégia de split:** 70/30 estratificado por classe, seed=42
- **Pré-processamento:** Imputação automática (mediana/moda); encoding categórico ordinal; normalização interna do pytabkit

| Dataset                          | Task ID | n      | Features | Classes | Regime |
| -------------------------------- | ------- | ------ | -------- | ------- | ------ |
| blood-transfusion-service-center | 10101   | 748    | 4        | 2       | small  |
| diabetes                         | 37      | 768    | 8        | 2       | small  |
| balance-scale                    | 11      | 625    | 4        | 3       | small  |
| credit-g                         | 31      | 1.000  | 20       | 2       | medium |
| phoneme                          | 9952    | 5.404  | 5        | 2       | medium |
| cmc                              | 23      | 1.473  | 9        | 3       | medium |
| adult                            | 7592    | 48.842 | 14       | 2       | large  |
| bank-marketing                   | 14965   | 45.211 | 16       | 2       | large  |
| connect-4                        | 146195  | 67.557 | 42       | 3       | large  |

---

## 6. Dados de treino e pré-treino

- **O modelo é treinado do zero** — não é um foundation model pré-treinado
- **Origem dos dados de treino:** 70% de cada dataset, com 5-fold CV no conjunto de treino para seleção de hiperparâmetros (defaults TD do pytabkit)
- **Possíveis vieses:** Dependem exclusivamente dos dados de cada dataset; não há viés herdado de pré-treino

---

## 7. Análise quantitativa

- **Posição no ranking médio:** #1 de 4 (AUC OVO médio = 0,8730 vs. CatBoost 0,8542, LightGBM 0,8511, XGBoost 0,8353)
- **Delta médio em AUC OVO vs. baselines:**
  - vs. LightGBM: +0,0219
  - vs. CatBoost: +0,0188
  - vs. XGBoost: +0,0377
- **Datasets em que TabM é #1 (7/9):** balance-scale, diabetes, phoneme, cmc, bank-marketing, connect-4, blood-transfusion (#2)
- **Datasets em que TabM perde:** credit-g (#3) e adult (#4 — único com missing values)
- **Custo vs. desempenho:** Tempo médio do TabM = 642,7 s vs. LightGBM = 0,9 s, CatBoost = 2,6 s, XGBoost = 1,1 s. O TabM é ~700× mais lento que LightGBM, mas entrega +2,2 pp de AUC OVO — trade-off desfavorável para produção, aceitável para pesquisa.
- **Quebra por regime:**
  - **Small:** TabM AUC=0,8721 — melhor resultado. O ensemble implícito reduz variância mesmo com n < 1k.
  - **Medium:** TabM AUC=0,8193 — empatado com CatBoost (0,8198); levemente acima de LightGBM e XGBoost.
  - **Large:** TabM AUC=0,9275 — melhor, mas custo >900 s/dataset torna o uso impraticável sem GPU.

---

## 8. Avisos e recomendações

- **Quando usar:** Regime médio (1k–10k amostras), features predominantemente numéricas, quando GPU está disponível
- **Quando NÃO usar:**
  - Aplicações com restrição de latência ou sem GPU para n > 20k
  - Datasets com muitos missing values sem pipeline de imputação dedicado
  - Aplicações que exigem interpretabilidade nativa (preferir EBM)
- **Alternativas recomendadas:**
  - Large sem GPU → LightGBM TD ou CatBoost TD
  - Interpretabilidade → EBM

---

## 9. Considerações éticas

- TabM é caixa-preta; não deve ser usado em decisões de alto impacto sem camada de XAI (SHAP, LIME)
- O dataset adult contém atributos sensíveis (sexo, raça); modelos treinados nele devem ser auditados para viés antes de qualquer uso real
- Impacto ambiental: tempo total de execução ≈ 5.785 s (≈ 1,6 h de CPU) nos 9 datasets
- Escopo deste trabalho: exclusivamente acadêmico

---

## 10. Reprodutibilidade

- **Ambiente:** Python 3.11, dependências fixadas em `pyproject.toml` (uv)
- **Seed:** 42 em todas as etapas (split, treino, tuning)
- **Comandos:**
  ```bash
  git clone <repo>
  cd projeto-am
  uv sync
  uv run python -m src.pipeline.run_all --include-group-model --seed 42
  jupyter nbconvert --to notebook --execute notebooks/04_analise_resultados.ipynb
  ```

---

## Referências

- Gorishniy, Y. et al. (2025). TabM: Advancing Tabular Deep Learning with Parameter-Efficient Ensembling. ICLR 2025. https://arxiv.org/abs/2410.24210
- Mitchell, M. et al. (2019). Model Cards for Model Reporting. FAT*.
- Erickson, N. et al. (2025). TabArena: A Living Benchmark. NeurIPS 2025.
