"""
Re-creates data/cicids2017_friday_ddos_sample.csv from the full CICIDS2017 file.

Input : Friday-WorkingHours-Afternoon-DDos.pcap_ISCX.csv
        (CICIDS2017, MachineLearningCVE folder, 225,745 rows, 79 columns)
Output: 5,000 rows = 4,750 BENIGN + 250 DDoS, all 79 original columns, values unchanged.

Usage:  python tools/make_sample.py path/to/Friday-WorkingHours-Afternoon-DDos.pcap_ISCX.csv
"""
import sys
from pathlib import Path

import pandas as pd

SEED = 42
N_BENIGN = 4750
N_DDOS = 250

src = Path(sys.argv[1])
out = Path(__file__).resolve().parent.parent / "data" / "cicids2017_friday_ddos_sample.csv"

df = pd.read_csv(src, low_memory=False)
label_col = [c for c in df.columns if c.strip() == "Label"][0]
labels = df[label_col].str.strip()

benign = df[labels == "BENIGN"].sample(N_BENIGN, random_state=SEED)
ddos = df[labels == "DDoS"].sample(N_DDOS, random_state=SEED)
sample = pd.concat([benign, ddos]).sample(frac=1, random_state=SEED)  # shuffle rows

sample.to_csv(out, index=False)
print(f"Full file: {len(df):,} rows, {df.shape[1]} columns")
print(labels.value_counts().to_string())
print(f"Saved {len(sample):,} rows to {out}")
