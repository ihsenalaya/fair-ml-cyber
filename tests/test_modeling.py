from sklearn.pipeline import Pipeline

from fair_ml_cyber.modeling import build_model


def test_logistic_regression_uses_high_iteration_budget():
    model = build_model("logistic_regression", seed=7)

    assert isinstance(model, Pipeline)
    assert model.named_steps["model"].max_iter == 2000
