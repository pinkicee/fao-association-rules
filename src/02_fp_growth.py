import pandas as pd
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import fpgrowth, association_rules

from config import (
    MIN_SUPPORT,
    MIN_CONFIDENCE,
    MIN_LIFT,
    MAX_ANTECEDENT_LEN,
    CONSEQUENT_LEN,
    RARE_ITEM_SUPPORT_THRESHOLD,
    PROCESSED_DIR
)
from utils import (
    ensure_dirs,
    load_merged_df,
    build_transactions,
    filter_rare_items,
    timed
)


def main():
    # =========================
    # 1. Pregatire date
    # =========================
    print("[INFO] Incarcare si pregatire date...")
    ensure_dirs()
    df = load_merged_df()

    # =========================
    # 2. Construire tranzactii
    # =========================
    transactions = build_transactions(df)
    print(f"[INFO] Tranzactii initiale: {len(transactions)}")

    # =========================
    # 3. Filtrare ingrediente rare
    # =========================
    transactions, kept_items = filter_rare_items(
        transactions,
        RARE_ITEM_SUPPORT_THRESHOLD
    )
    print(f"[INFO] Tranzactii dupa filtrare: {len(transactions)}")
    print(f"[INFO] Ingrediente pastrate: {len(kept_items)}")

    # =========================
    # 4. One-hot encoding
    # =========================
    print("[INFO] One-hot encoding...")
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
    t_fp, frequent_itemsets = timed(
        fpgrowth,
        basket,
        min_support=MIN_SUPPORT,
        use_colnames=True
    )
    print(f"[INFO] FP-Growth finalizat in {round(t_fp, 2)} secunde")
    print(f"[INFO] Itemset-uri frecvente: {len(frequent_itemsets)}")

    # =========================
    # 6. Generare reguli
    # =========================
    print("[INFO] Generare reguli de asociere...")
    t_rules, rules = timed(
        association_rules,
        frequent_itemsets,
        metric="confidence",
        min_threshold=MIN_CONFIDENCE
    )
    print(f"[INFO] Reguli generate (initial): {len(rules)}")

    # =========================
    # 7. Limitare si filtrare reguli
    # =========================
    print("[INFO] Aplicare filtre pe reguli...")
    rules = rules[
        (rules["antecedents"].apply(len) <= MAX_ANTECEDENT_LEN) &
        (rules["consequents"].apply(len) == CONSEQUENT_LEN) &
        (rules["lift"] >= MIN_LIFT)
        ].sort_values(["lift", "confidence"], ascending=False)

    # Conversie pentru afisare
    rules["antecedents"] = rules["antecedents"].apply(
        lambda x: ", ".join(sorted(x))
    )
    rules["consequents"] = rules["consequents"].apply(
        lambda x: ", ".join(sorted(x))
    )

    print(f"[INFO] Reguli finale dupa filtrare: {len(rules)}")

    # =========================
    # 8. Afisare rezultate
    # =========================
    print("\n===== TOP 10 REGULI =====")
    print(
        rules[
            ["antecedents", "consequents", "support", "confidence", "lift"]
        ].head(10)
    )

    # =========================
    # 9. Salvare rezultate
    # =========================
    rules.to_csv(PROCESSED_DIR / "fp_rules_limited.csv", index=False)
    frequent_itemsets.to_csv(
        PROCESSED_DIR / "fp_frequent_itemsets.csv",
        index=False
    )

    print("\n[INFO] Rezultate salvate in data/processed/")
    print("[INFO] Proces finalizat cu succes.")


if __name__ == "__main__":
    main()
