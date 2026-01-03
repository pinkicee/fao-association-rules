import time
import pandas as pd

from config import CONSUMPTION_CSV, SUBJECT_CSV, PROCESSED_DIR


def ensure_dirs():
    # Creeaza directorul pentru rezultate
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)


def load_merged_df():
    # Incarca datele si face join pe SUBJECT
    cons = pd.read_csv(CONSUMPTION_CSV, low_memory=False)
    subj = pd.read_csv(SUBJECT_CSV, low_memory=False)

    cons = cons[["SUBJECT", "SURVEY_DAY", "INGREDIENT"]].dropna()
    subj = subj[["SUBJECT", "ADM0_NAME"]].dropna()

    df = cons.merge(subj, on="SUBJECT", how="inner")

    # Curata denumirile ingredientelor
    df["INGREDIENT"] = df["INGREDIENT"].astype(str).str.strip().str.lower()
    return df


def build_transactions(df):
    # Tranzactie = (SUBJECT, SURVEY_DAY)
    return (
        df.groupby(["SUBJECT", "SURVEY_DAY"])["INGREDIENT"]
        .apply(lambda x: set(x))
        .tolist()
    )


def filter_rare_items(transactions, support_threshold):
    # Elimina ingredientele cu suport mic
    n = len(transactions)
    min_count = int(support_threshold * n)

    counts = {}
    for t in transactions:
        for item in t:
            counts[item] = counts.get(item, 0) + 1

    kept_items = {i for i, c in counts.items() if c >= min_count}

    filtered = [
        sorted(t.intersection(kept_items))
        for t in transactions
        if len(t.intersection(kept_items)) > 1
    ]

    return filtered, kept_items


def timed(func, *args, **kwargs):
    # Masoara timpul de executie
    start = time.time()
    result = func(*args, **kwargs)
    return time.time() - start, result
