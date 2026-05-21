"""Placeholder do modelo principal do grupo.

Cada grupo deve substituir `build_group_model` pelo wrapper sklearn-compatível
do modelo atribuído. A lista de modelos atribuíveis está descrita no README.

Padrão esperado: a função retorna um estimador com .fit(X, y) e .predict_proba(X).
Se o modelo não tem API sklearn, envolva em sklearn.base.BaseEstimator.
"""

from __future__ import annotations


def build_group_model(seed: int = 42):
    # 3) TabM (via pytabkit)
    from pytabkit import TabM_D_Classifier
    return TabM_D_Classifier(random_state=seed)