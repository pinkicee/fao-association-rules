import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter

from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import fpgrowth, association_rules

from config import (
    PROCESSED_DIR,
    MIN_SUPPORT,
    MIN_CONFIDENCE,
    MIN_LIFT,
    MAX_ANTECEDENT_LEN,
    CONSEQUENT_LEN,
    RARE_ITEM_SUPPORT_THRESHOLD
)

from utils import (
    ensure_dirs,
    load_merged_df_multi,
    filter_rare_items,
    timed
)


def main():
    print("[INFO] Analiza combinata RO + LAO")

    ensure_dirs()

    OUT_DIR = PROCESSED_DIR / "combined"
    FIG_DIR = OUT_DIR / "figures"
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    FIG_DIR.mkdir(parents=True, exist_ok=True)

    # =========================
    # 1. Incarcare date
    # =========================
    df = load_merged_df_multi()

    print("[INFO] Nr tari:", df["COUNTRY"].nunique())
    print("[INFO] Nr subiecti:", df["SUBJECT"].nunique())
    print("[INFO] Nr ingrediente unice:", df["INGREDIENT"].nunique())

    # =========================
    # 2. Tranzactii
    # =========================
    transactions_df = (
        df.groupby(["COUNTRY", "SUBJECT", "SURVEY_DAY"])["INGREDIENT"]
        .apply(lambda x: set(x))
        .reset_index(name="items")
    )

    transactions_df["length"] = transactions_df["items"].apply(len)
    transactions = transactions_df["items"].tolist()

    print("[INFO] Tranzactii totale:", len(transactions))

    transactions_df.to_csv(
        OUT_DIR / "transactions_combined.csv",
        index=False
    )

    # =========================
    # 3. Filtrare itemi rari
    # =========================
    transactions, kept_items = filter_rare_items(
        transactions,
        RARE_ITEM_SUPPORT_THRESHOLD
    )

    print("[INFO] Tranzactii dupa filtrare:", len(transactions))
    print("[INFO] Ingrediente pastrate:", len(kept_items))

    # =========================
    # 4. One-hot encoding
    # =========================
    te = TransactionEncoder()
    basket = pd.DataFrame(
        te.fit(transactions).transform(transactions),
        columns=te.columns_,
        dtype=bool
    )

    # =========================
    # 5. FP-Growth
    # =========================
    print("[INFO] Rulare FP-Growth...")
    t_fp, freq_itemsets = timed(
        fpgrowth,
        basket,
        min_support=MIN_SUPPORT,
        use_colnames=True
    )

    print(f"[INFO] FP-Growth finalizat in {round(t_fp, 2)} secunde")
    print("[INFO] Itemset-uri frecvente:", len(freq_itemsets))

    freq_itemsets.to_csv(
        OUT_DIR / "fp_frequent_itemsets_combined.csv",
        index=False
    )

    # =========================
    # 6. Reguli de asociere
    # =========================
    _, rules = timed(
        association_rules,
        freq_itemsets,
        metric="confidence",
        min_threshold=MIN_CONFIDENCE
    )

    rules = rules[
        (rules["antecedents"].apply(len) <= MAX_ANTECEDENT_LEN) &
        (rules["consequents"].apply(len) == CONSEQUENT_LEN) &
        (rules["lift"] >= MIN_LIFT)
    ].sort_values(["lift", "confidence"], ascending=False)

    rules["antecedents"] = rules["antecedents"].apply(
        lambda x: ", ".join(sorted(x))
    )
    rules["consequents"] = rules["consequents"].apply(
        lambda x: ", ".join(sorted(x))
    )

    rules.to_csv(
        OUT_DIR / "fp_rules_combined.csv",
        index=False
    )

    print("[INFO] Reguli finale:", len(rules))

    # =========================
    # 7. Grafice
    # =========================
    print("[INFO] Salvare grafice...")

    # 7.1 Lungimea tranzactiilor
    plt.figure()
    transactions_df["length"].hist(bins=20)
    plt.xlabel("Numar ingrediente / tranzactie")
    plt.ylabel("Frecventa")
    plt.title("Distributia lungimii tranzactiilor (RO + LAO)")
    plt.tight_layout()
    plt.savefig(FIG_DIR / "transaction_length_distribution.png")
    plt.close()

    # 7.2 Top ingrediente
    counter = Counter()
    for t in transactions:
        counter.update(t)

    items, counts = zip(*counter.most_common(15))

    plt.figure()
    plt.barh(items, counts)
    plt.xlabel("Frecventa")
    plt.title("Top 15 ingrediente frecvente (RO + LAO)")
    plt.tight_layout()
    plt.savefig(FIG_DIR / "top_ingredients_combined.png")
    plt.close()

    # 7.3 Confidence vs Lift
    plt.figure()
    plt.scatter(rules["confidence"], rules["lift"], alpha=0.4)
    plt.xlabel("Confidence")
    plt.ylabel("Lift")
    plt.title("Distributia regulilor de asociere (RO + LAO)")
    plt.tight_layout()
    plt.savefig(FIG_DIR / "confidence_vs_lift_combined.png")
    plt.close()

    print("[INFO] Analiza combinata finalizata cu succes.")
    print("[INFO] Grafice salvate in:", FIG_DIR)


if __name__ == "__main__":
    main()
