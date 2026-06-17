import pandas as pd

from fair_ml_cyber.plots import plot_per_class_heatmap, plot_split_gap


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


def test_plot_per_class_heatmap_writes_png(tmp_path):
    rows = []
    for split, web_f1 in [("random_stratified", 0.8), ("scenario_holdout_Web", 0.0)]:
        rows.extend(
            [
                {
                    "model": "hist_gradient_boosting",
                    "split": split,
                    "label": "Benign",
                    "f1": 0.95,
                    "support": 100,
                },
                {
                    "model": "hist_gradient_boosting",
                    "split": split,
                    "label": "Web_XSS",
                    "f1": web_f1,
                    "support": 20,
                },
            ]
        )
    per_class = tmp_path / "per_class.csv"
    pd.DataFrame(rows).to_csv(per_class, index=False)

    output = tmp_path / "heatmap.png"
    result = plot_per_class_heatmap(per_class, output, model="hist_gradient_boosting")

    assert result["figure_path"] == str(output)
    assert output.exists()
    assert output.stat().st_size > 0
