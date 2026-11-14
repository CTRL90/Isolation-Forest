"""
Basic checks. Run from the project folder:  python tests/test_app.py
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

import numpy as np
from sklearn.ensemble import IsolationForest
from streamlit.testing.v1 import AppTest

import demo
import iforest_from_scratch as scratch


def test_data_and_model():
    df = demo.load_raw()
    assert len(df) == 5000 and df.shape[1] == 79
    assert set(df["Label"]) == {"BENIGN", "DDoS"}
    X, labels, rep = demo.preprocess(df)
    assert "Label" not in X.columns and list(X.columns) == demo.FEATURES
    assert np.isfinite(X.values).all()
    model, pred, score, decision = demo.run_isolation_forest(X)
    assert set(np.unique(pred)) <= {-1, 1}
    assert (pred == -1).sum() == round(0.05 * len(X))           # contamination = 0.05
    assert np.allclose(score, -model.score_samples(X))
    assert np.array_equal(pred == -1, decision < 0)              # predict follows decision_function
    assert ((score > 0) & (score <= 1)).all()
    # same seed -> same result
    _, pred2, _, _ = demo.run_isolation_forest(X)
    assert np.array_equal(pred, pred2)
    print("data/model OK:", rep, "anomalies:", int((pred == -1).sum()))


def test_scratch_matches_theory():
    # c(n) values and the 0.5 point of the score
    assert scratch.c(1) == 0 and scratch.c(2) == 1
    assert abs(scratch.c(256) - 10.2448) < 1e-3
    rs = np.random.RandomState(0)
    data = rs.normal(size=(500, 2)).tolist() + [[8.0, 8.0]]
    forest, psi = scratch.iforest(data, t=100, psi=256, seed=1)
    s_out = scratch.anomaly_score([8.0, 8.0], forest, psi)
    s_in = scratch.anomaly_score([0.0, 0.0], forest, psi)
    sk = IsolationForest(n_estimators=100, max_samples=256, random_state=1).fit(np.array(data))
    sk_out, sk_in = -sk.score_samples([[8.0, 8.0], [0.0, 0.0]])
    assert s_out > 0.6 > 0.5 > s_in
    assert abs(s_out - sk_out) < 0.08 and abs(s_in - sk_in) < 0.08
    print(f"scratch vs sklearn: outlier {s_out:.3f} / {sk_out:.3f}, centre {s_in:.3f} / {sk_in:.3f}")


def test_app_runs_and_button():
    at = AppTest.from_file(str(ROOT / "app.py"), default_timeout=120).run()
    assert not at.exception, at.exception
    assert len(at.button) == 1 and at.button[0].label == "Run Detection"
    at.button[0].click().run()
    assert not at.exception, at.exception
    metrics = {m.label: m.value for m in at.metric}
    assert metrics["Normal (prediction = 1)"] == "4,750"
    assert metrics["Anomalies (prediction = −1)"] == "250"
    print("app OK, metrics:", metrics)


if __name__ == "__main__":
    test_data_and_model()
    test_scratch_matches_theory()
    test_app_runs_and_button()
    print("All tests passed.")
