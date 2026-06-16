import numpy as np

from fair_ml_cyber.metrics import binary_metrics, expected_calibration_error, transferability_score


def test_binary_metrics_basic():
    y = np.array([0, 0, 1, 1])
    p = np.array([0.1, 0.2, 0.8, 0.9])
    m = binary_metrics(y, p)
    assert m["macro_f1"] == 1.0
    assert m["mcc"] == 1.0
    assert m["auroc"] == 1.0


def test_ece_range():
    ece = expected_calibration_error(np.array([0, 1]), np.array([0.2, 0.8]))
    assert 0.0 <= ece <= 1.0


def test_transferability_score():
    assert transferability_score(0.8, 1.0) == 0.8
    assert transferability_score(0.8, 0.0) is None

