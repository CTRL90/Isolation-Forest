# Isolation Forest: Course Project Website

Course: Design and Analysis of Algorithms

## 1. Project purpose

This website explains the **Isolation Forest (iForest)** algorithm (Liu, Ting and Zhou, 2008): what it is, how it works, the anomaly score, main parameters, applications, advantages and disadvantages, pseudocode, and time complexity. The website is organized around the algorithm: Introduction, How It Works, Applications, Pseudocode, Time Complexity. After these sections there is one additional practical example (network traffic anomaly detection) that runs scikit-learn's `IsolationForest` on a real sample of the CICIDS2017 dataset.

The algorithm is the subject of the project. The example is optional.

## 2. Installation requirements

- Python 3.9 or newer
- The packages in `requirements.txt` (Streamlit, pandas, NumPy, scikit-learn, Altair)

```bash
pip install -r requirements.txt
```

## 3. Running locally

From the project folder:

```bash
streamlit run app.py
```

Then open the address shown in the terminal (usually http://localhost:8501).

Optional checks:

```bash
python tests/test_app.py
```

Group and university details are in `PROJECT_INFO` at the top of `app.py` (the instructor name is still a placeholder).

## 4. Dataset source

- **Dataset:** CICIDS2017, Canadian Institute for Cybersecurity, University of New Brunswick
- **Official page:** https://www.unb.ca/cic/datasets/ids-2017.html
- **File:** `Friday-WorkingHours-Afternoon-DDos.pcap_ISCX.csv` (MachineLearningCVE)
- **Bundled sample:** `data/cicids2017_friday_ddos_sample.csv`, 5,000 rows (4,750 BENIGN, 250 DDoS), all 79 original columns, random seed 42

How the file was obtained and checked, and how the sample was made, is described in `data/DATA_SOURCE.md`. `tools/make_sample.py` re-creates the sample from the full file. No download is needed when the app runs.

## 5. Project structure

```
Isolation_Forest_Website/
├── app.py                      Streamlit website (academic sections + additional example)
├── content.py                  Academic text, tables, equations and pseudocode
├── demo.py                     Data loading, preprocessing and Isolation Forest for the example
├── iforest_from_scratch.py     The paper's pseudocode written in plain Python (for learning and checks)
├── requirements.txt
├── README.md
├── .streamlit/config.toml      Theme (ivory, muted gold, charcoal)
├── assets/                     Figures used in the website
├── data/
│   ├── cicids2017_friday_ddos_sample.csv
│   └── DATA_SOURCE.md
├── tests/test_app.py           Checks for data, model, from-scratch code and the app
└── tools/                      Scripts that made the sample and the figures (not needed to run the app)
```

## 6. Deployment (GitHub + Streamlit Community Cloud)

1. Create a new GitHub repository and upload the contents of this folder (keep the folder structure, including `.streamlit/`, `assets/` and `data/`).
2. Go to https://share.streamlit.io and sign in with GitHub.
3. Click **Create app**, choose the repository and branch, and set the main file path to `app.py`.
4. Click **Deploy**. Streamlit Cloud installs `requirements.txt` automatically.
5. Copy the app URL and paste it into the "Interactive Practical Demonstration" section of the Word report.

All paths in the code are relative to the project folder, so nothing depends on a local computer.
