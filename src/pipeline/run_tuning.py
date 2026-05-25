from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

from data.load_tabarena import RECOMMENDED_TASK_IDS, load_task
from src.pipeline.split import stratified_split
from src.pipeline.tune import tabm_factory, tabm_search_space, tune


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--n-trials", type=int, default=30)
    parser.add_argument("--cv-folds", type=int, default=3)
    parser.add_argument(
        "--task-ids", type=int, nargs="*", default=None,
        help="lista de task IDs; se omitido usa todos os RECOMMENDED_TASK_IDS",
    )
    parser.add_argument("--output", type=Path, default=Path("results/tuning_results.csv"))
    parser.add_argument("--trials-output", type=Path, default=Path("results/tuning_trials.csv"))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    args.output.parent.mkdir(parents=True, exist_ok=True)

    task_ids = args.task_ids if args.task_ids else RECOMMENDED_TASK_IDS
    best_rows: list[dict] = []
    trial_rows: list[dict] = []

    for task_id in task_ids:
        ds = load_task(task_id)
        X_train, _, y_train, _ = stratified_split(ds.X, ds.y, seed=args.seed)

        print(f"\n[{ds.name}] iniciando tuning ({args.n_trials} trials)...")
        best_params, best_auc, study = tune(
            estimator_factory=tabm_factory,
            search_space=tabm_search_space,
            X=X_train,
            y=y_train,
            seed=args.seed,
            n_trials=args.n_trials,
            cv_folds=args.cv_folds,
        )
        print(f"[{ds.name}] melhor AUC={best_auc:.4f} | params={best_params}")

        best_rows.append({"task_id": task_id, "dataset": ds.name, "best_auc_cv": best_auc, **best_params})

        for trial in study.trials:
            trial_rows.append({
                "task_id": task_id,
                "dataset": ds.name,
                "trial": trial.number,
                "auc_cv": trial.value,
                **trial.params,
            })

    pd.DataFrame(best_rows).to_csv(args.output, index=False)
    pd.DataFrame(trial_rows).to_csv(args.trials_output, index=False)
    print(f"\nResultados salvos em {args.output} e {args.trials_output}")


if __name__ == "__main__":
    main()