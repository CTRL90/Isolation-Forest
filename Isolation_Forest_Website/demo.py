"""
Practical demonstration: data loading, preprocessing and Isolation Forest.

Everything here runs on the bundled CICIDS2017 sample. Nothing is hardcoded:
the counts, charts and tables in the app come from the model output.
"""
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest

DATA_PATH = Path(__file__).parent / "data" / "cicids2017_friday_ddos_sample.csv"
DATASET_NAME = "CICIDS2017 (Friday-WorkingHours-Afternoon-DDos, MachineLearningCVE)"
SOURCE_URL = "https://www.unb.ca/cic/datasets/ids-2017.html"

RANDOM_SEED = 42

# Numeric flow features chosen on domain grounds (size, rate and timing of a flow).
# Ports, IP addresses and the Label column are not used for training.
FEATURES = [
    "Flow Duration",
    "Total Fwd Packets",
    "Total Backward Packets",
    "Total Length of Fwd Packets",
    "Total Length of Bwd Packets",
    "Fwd Packet Length Max",
    "Bwd Packet Length Max",
    "Bwd Packet Length Mean",
    "Flow Bytes/s",
    "Flow Packets/s",
    "Flow IAT Mean",
    "Fwd IAT Std",
    "Packet Length Std",
    "Average Packet Size",
    "Init_Win_bytes_forward",
]

MODEL_PARAMS = {
    "n_estimators": 100,     # t, number of trees (paper default)
    "max_samples": 256,      # psi, sub-sample size (paper default)
    "contamination": 0.05,   # expected share of anomalies, sets the threshold
    "max_features": 1.0,     # each tree sees all selected features
    "random_state": RANDOM_SEED,
}


def load_raw(path=DATA_PATH):
    """Read the CSV and remove the extra spaces in the original column names."""
    df = pd.read_csv(path, low_memory=False)
    df.columns = df.columns.str.strip()
    df["Label"] = df["Label"].astype(str).str.strip()
    return df


def preprocess(df):
    """
    Keep the selected numeric features, turn +/-inf into NaN and drop rows that
    are not usable. The Label column is kept aside and never used for training.
    Returns X (features), labels (for the optional evaluation only) and a small report.
    """
    report = {"rows_in": len(df)}
    X = df[FEATURES].apply(pd.to_numeric, errors="coerce")
    X = X.replace([np.inf, -np.inf], np.nan)
    bad = X.isna().any(axis=1)
    report["rows_removed"] = int(bad.sum())
    X = X[~bad].reset_index(drop=True)
    labels = df.loc[~bad, "Label"].reset_index(drop=True)
    report["rows_out"] = len(X)
    report["n_features"] = X.shape[1]
    return X, labels, report


def run_isolation_forest(X):
    """Train sklearn's IsolationForest on X and return predictions and scores."""
    model = IsolationForest(**MODEL_PARAMS)
    model.fit(X)
    pred = model.predict(X)                 # 1 = normal, -1 = anomaly
    paper_score = -model.score_samples(X)   # s(x, psi) from the paper, in (0, 1]
    decision = model.decision_function(X)   # < 0 means anomaly
    return model, pred, paper_score, decision
