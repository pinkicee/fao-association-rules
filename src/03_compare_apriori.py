import pandas as pd
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import fpgrowth, apriori

from config import *
from utils import (
    ensure_dirs,
    load_merged_df,
    build_transactions,
    filter_rare_items,
    timed
)


def main():
    # =========================
    # 1. Incarcare si pregatire date
    # =========================
    print("[INFO] Incarcare date...")
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
    # 5. Rulare FP-Growth
    # =========================
    print("[INFO] Rulare FP-Growth...")
    t_fp, freq_fp = timed(
        fpgrowth,
        basket,
        min_support=MIN_SUPPORT,
        use_colnames=True
    )
    print(f"[INFO] FP-Growth finalizat in {round(t_fp, 2)} secunde")
    print(f"[INFO] Itemset-uri FP-Growth: {len(freq_fp)}")

    # =========================
    # 6. Rulare Apriori (comparativ)
    # =========================
    print("[INFO] Rulare Apriori...")
    try:
        t_ap, freq_ap = timed(
            apriori,
            basket,
            min_support=MIN_SUPPORT,
            use_colnames=True
        )
        print(f"[INFO] Apriori finalizat in {round(t_ap, 2)} secunde")
        print(f"[INFO] Itemset-uri Apriori: {len(freq_ap)}")

        # Raport comparativ
        if t_fp > 0:
            print(
                f"[INFO] FP-Growth a fost de aproximativ "
                f"{round(t_ap / t_fp, 2)} ori mai rapid decat Apriori"
            )
    except:
        print("[WARN] Apriori nu a rulat din motive de resurse.")

    print("[INFO] Comparatia algoritmilor a fost finalizata.")


if __name__ == "__main__":
    main()
