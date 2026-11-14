# Dataset source and sampling

## Dataset

**CICIDS2017** (Intrusion Detection Evaluation Dataset), Canadian Institute for Cybersecurity (CIC), University of New Brunswick.

- Official page: https://www.unb.ca/cic/datasets/ids-2017.html
- Dataset paper: Sharafaldin, I., Habibi Lashkari, A., and Ghorbani, A. A. (2018). Toward Generating a New Intrusion Detection Dataset and Intrusion Traffic Characterization. ICISSP 2018, pp. 108–116.

## File used

`Friday-WorkingHours-Afternoon-DDos.pcap_ISCX.csv` from the `MachineLearningCVE` folder (the CSV release produced with CICFlowMeter).

The official download on the UNB page goes through a request form, so the file was taken from a public GitHub mirror that states it is the unmodified official file:

- Mirror: https://github.com/RohithDharshan/Cloud-DDoS-Detector (file `data/raw/Friday-WorkingHours-Afternoon-DDoS.pcap_ISCX.csv`, commit `5b0900c`)
- Size: 77,123,859 bytes
- SHA-256: `6ff1580f5f81c0ae28a26f7631721018577f5f7c5e0feac28b795fcfe7b411ee`

## How the file was checked

We could not compare it byte-by-byte with the UNB download (form-gated). We checked it against facts reported independently for the official file:

| Check | Value in our file | Matches |
|---|---|---|
| Rows | 225,745 | Row count listed for this file in other public CICIDS2017 projects |
| Columns | 79 (78 flow features + `Label`, original header spacing kept) | Official MachineLearningCVE layout |
| Labels | BENIGN 97,718 and DDoS 128,027 | Counts reported by independent notebooks |
| File size | 77.1 MB | Size shown for the same file on two Hugging Face mirrors |

## Sample bundled with the app

`cicids2017_friday_ddos_sample.csv`

- 5,000 rows: 4,750 BENIGN + 250 DDoS (5% attacks)
- All 79 original columns, values not changed
- Random selection without replacement, `random_state = 42`, then rows shuffled
- SHA-256: `20911072b1f653b8e2af561d381dda27a58498063affd54b75a3ad32c7e34e77`

Why 5% attacks: in the full Friday afternoon file, DDoS flows are the majority (about 57%). Isolation Forest assumes anomalies are few, so we kept the attacks rare on purpose. This is a design choice for the demonstration, and it is stated in the app.

The script `tools/make_sample.py` re-creates this sample from the full file.
