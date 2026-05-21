# Model Card: TabM

> Estrutura inspirada em Mitchell et al. (2019), com extensões específicas da disciplina.
> Campos marcados com `<...>` devem ser preenchidos após os experimentos.

---

## 1. Detalhes do modelo

- **Nome:** TabM
- **Versão:** 1.0 (ICLR 2025)
- **Autores originais:** Gorishniy et al., Yandex Research, 2025
- **Repositório oficial:** https://github.com/yandex-research/tabm
- **Licença do código:** Apache 2.0
- **Família arquitetural:** Ensemble parameter-efficient de MLPs com k cabeças independentes e pesos compartilhados
- **Contagem de parâmetros:** `<preencher após experimentos — inspecionar com sum(p.numel() for p in model.parameters())>`
- **Complexidade computacional:** O(n · p · k) em treino, onde k=32 cabeças; inferência O(p · k) por amostra
- **Pico de memória observado:** `<preencher após experimentos — monitorar via psutil ou nvidia-smi>`
- **Toolkit / dependências:** pytabkit 1.7.3, torch 2.7.1, scikit-learn 1.8.0
- **Hiperparâmetros principais:** `num_emb_type` ∈ {none, pbld, plr}, `n_epochs` ∈ [50, 200], `lr` ∈ [1e-4, 1e-2] — busca via Optuna (TPE, 5-fold CV)

---

## 2. Uso pretendido

- **Caso de uso primário:** Classificação supervisionada em dados tabulares IID binários e multiclasse
- **Casos de uso fora de escopo:** Dados não-IID, séries temporais, dados de imagem, texto ou áudio
- **Usuários pretendidos:** Pesquisadores e praticantes em problemas tabulares com benchmarks padronizados
- **Faixa de n suportada:** Até ~50.000 amostras com bom desempenho em CPU; datasets maiores requerem GPU
- **Faixa de p suportada:** Até ~500 features após codificação; testado com até 42 features neste projeto
- **Condições operacionais:** Roda em laptop com 8 GB de RAM sem GPU; GPU recomendada para n > 20.000

---

## 3. Fatores observados

Dimensões em que o desempenho do modelo varia, avaliadas sobre os 9 datasets do TabArena-v0.1:

- **Tamanho do dataset (n):** Ponto forte no regime médio (1k–10k), onde o ensemble implícito reduz variância. No regime pequeno, foundation models (TabPFN) tendem a superar. No regime grande sem GPU, GBM costuma ser mais eficiente. `<confirmar com resultados>`
- **Número de classes:** `<preencher — comparar AUC OVO em binário vs. multiclasse>`
- **Proporção entre features categóricas e numéricas:** Features numéricas beneficiam diretamente dos embeddings pbld/plr. Alta proporção categórica (ex: connect-4, 42 de 42 features) pode limitar o ganho dos embeddings. `<confirmar com resultados>`
- **Presença de valores ausentes:** Pipeline aplica imputação automática (mediana para numéricas, moda para categóricas). Impacto isolado observado no dataset adult (task 7592). `<preencher com resultado>`

---

## 4. Métricas alcançadas

Tabela agregada nos 9 datasets do TabArena-v0.1. Média, desvio padrão e IC 95% via bootstrap (1.000 reamostragens).

| Métrica         | Média      | Desvio     | IC 95% (bootstrap)   |
| --------------- | ---------- | ---------- | -------------------- |
| AUC OvO         | `<0,0000>` | `<0,0000>` | `<[0,0000; 0,0000]>` |
| Accuracy        | `<0,0000>` | `<0,0000>` | `<[0,0000; 0,0000]>` |
| G-Mean          | `<0,0000>` | `<0,0000>` | `<[0,0000; 0,0000]>` |
| Cross-Entropy   | `<0,0000>` | `<0,0000>` | `<[0,0000; 0,0000]>` |
| Tempo total (s) | `<0,0>`    | `<0,0>`    | `<[0,0; 0,0]>`       |

### Resultados por regime

- **Tamanho:** pequeno: AUC=`<...>`; médio: AUC=`<...>`; grande: AUC=`<...>`
- **Número de classes:** binário: AUC=`<...>`; multiclasse: AUC=`<...>`
- **Proporção categórica:** baixa (≤30%): AUC=`<...>`; alta (>30%): AUC=`<...>`
- **Missing values:** com NaN (adult): AUC=`<...>`; sem NaN (demais): AUC=`<...>`

---

## 5. Dados de avaliação

- **Origem:** 9 datasets do TabArena-v0.1 (NeurIPS 2025), carregados via OpenML (study 457)
- **Distribuição por regime:** 3 pequenos + 3 médios + 3 grandes
- **Estratégia de split:** 70/30 estratificado por classe, seed=42
- **Pré-processamento aplicado:** Imputação automática via pipeline do template (mediana/moda); encoding categórico ordinal; sem escalonamento explícito (pytabkit normaliza internamente)
- **Datasets utilizados:**

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
- **Origem dos dados de pré-treino:** N/A (pesos inicializados aleatoriamente com seed=42)
- **Origem dos dados de treino direto:** 70% de cada dataset do projeto, com validação cruzada 5-fold para seleção de hiperparâmetros
- **Possíveis vieses herdados do pré-treino:** N/A — por ser treinado do zero, vieses dependem exclusivamente dos dados de cada dataset

---

## 7. Análise quantitativa

- **Posição no ranking médio entre os 4 sistemas avaliados:** `<x de 4 — preencher após experimentos>`
- **Comparação com baselines:**
  - Delta médio em AUC OVO vs. LightGBM: `<preencher>`
  - Delta médio em AUC OVO vs. CatBoost: `<preencher>`
  - Delta médio em AUC OVO vs. XGBoost: `<preencher>`
  - Datasets em que TabM vence todos os baselines: `<preencher>`
  - Datasets em que TabM perde para algum baseline: `<preencher>`
- **Custo vs. desempenho:** Tempo total do TabM: `<x>` s vs. LightGBM: `<x>` s. `<descrever trade-off observado>`
- **Quebra por regime:**
  - Small: `<TabM ganha/perde; explicação>`
  - Medium: `<TabM ganha/perde; explicação>`
  - Large: `<TabM ganha/perde; explicação>`

---

## 8. Avisos e recomendações

- **Quando usar este modelo:** Regime médio (1k–10k amostras), mix de features numéricas e categóricas, quando GPU está disponível para datasets grandes
- **Quando NÃO usar este modelo:**
  - Datasets muito pequenos (< 500 amostras): preferir TabPFN ou LightGBM TD
  - Datasets muito grandes (> 50k) sem GPU: preferir LightGBM ou CatBoost por eficiência
  - Aplicações que exigem interpretabilidade: preferir EBM
  - Features categóricas de altíssima cardinalidade sem pré-processamento adequado
- **Alternativas recomendadas:**
  - Small sem GPU → LightGBM TD ou TabPFN
  - Large sem GPU → LightGBM TD ou CatBoost TD
  - Interpretabilidade exigida → EBM (modelo 9 da disciplina)

---

## 9. Considerações éticas

- **Riscos de uso indevido:** TabM é um modelo caixa-preta sem explicabilidade nativa; não deve ser usado em decisões de alto impacto (crédito, saúde, justiça) sem camada de XAI (SHAP, LIME)
- **Fairness por classe:** O dataset adult contém atributos sensíveis (sexo, raça, nacionalidade); modelos treinados nele devem ser auditados para viés antes de qualquer uso real. `<inserir recall por classe após experimentos>`
- **Impacto ambiental:** `<preencher com tempo total de tuning em segundos e estimativa de consumo energético>`
- **Recomendações de auditoria:** Comparar predições com baseline interpretável (EBM) em datasets sensíveis antes de qualquer deploy; monitorar G-Mean para detectar viés em classes minoritárias
- **Escopo deste trabalho:** Exclusivamente acadêmico; nenhum modelo foi implantado em produção

---

## 10. Reprodutibilidade

- **Ambiente:** Python 3.11.15, dependências fixadas em `pyproject.toml`
- **Hardware utilizado:** `<preencher — CPU, RAM, tempo total de execução>`
- **Comandos para reproduzir:**
  ```bash
  git clone https://github.com/aanasc4/projeto-am.git
  cd projeto-am
  uv sync
  uv run python -m src.pipeline.run_all --include-group-model --seed 42
  ```
- **Hash do commit:** `<git rev-parse HEAD — preencher na entrega final>`

---

## Referências

- Gorishniy, Y. et al. (2025). TabM: Advancing Tabular Deep Learning with Parameter-Efficient Ensembling. ICLR 2025. https://arxiv.org/abs/2410.24210
- Mitchell, M. et al. (2019). Model Cards for Model Reporting. FAT\*.
- Erickson, N. et al. (2025). TabArena: A Living Benchmark for Machine Learning on Tabular Data. NeurIPS 2025. https://arxiv.org/abs/2506.16791
- Holzmüller, D. (2024). pytabkit. https://github.com/dholzmueller/pytabkit
