import pandas as pd

from fair_ml_cyber.plots import plot_split_gap


def test_plot_split_gap_writes_png(tmp_path):
    rows = []
    for seed in [1, 2]:
        rows.extend(
            [
                {
                    "model": "logistic_regression",
                    "split": "random_stratified",
                    "seed": seed,
                    "status": "completed",
                    "macro_f1": 0.9,
                },
                {
                    "model": "logistic_regression",
                    "split": "temporal",
                    "seed": seed,
                    "status": "completed",
                    "macro_f1": 0.5,
                },
            ]
        )
    results = tmp_path / "results.csv"
    pd.DataFrame(rows).to_csv(results, index=False)

    output = tmp_path / "figure.png"
    result = plot_split_gap([results], output)

    assert result["figure_path"] == str(output)
    assert output.exists()
    assert output.stat().st_size > 0
