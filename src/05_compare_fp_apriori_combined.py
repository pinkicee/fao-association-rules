import pandas as pd
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import fpgrowth, apriori

from config import MIN_SUPPORT
from utils import load_merged_df_multi, filter_rare_items, timed


def main():
    print("[INFO] Comparatie FP-Growth vs Apriori (RO + LAO)")

    # =========================
    # 1. Incarcare date
    # =========================
    df = load_merged_df_multi()

    transactions = (
        df.groupby(["COUNTRY", "SUBJECT", "SURVEY_DAY"])["INGREDIENT"]
        .apply(lambda x: set(x))
        .tolist()
    )

    print("[INFO] Tranzactii initiale:", len(transactions))

    # =========================
    # 2. Filtrare itemi rari
    # =========================
    transactions, _ = filter_rare_items(transactions, MIN_SUPPORT)
    print("[INFO] Tranzactii dupa filtrare:", len(transactions))

    # =========================
    # 3. One-hot encoding
    # =========================
    te = TransactionEncoder()
    basket = pd.DataFrame(
        te.fit(transactions).transform(transactions),
        columns=te.columns_,
        dtype=bool
    )

    # =========================
    # 4. FP-Growth
    # =========================
    print("\n[INFO] Rulare FP-Growth...")
    t_fp, freq_fp = timed(
        fpgrowth,
        basket,
        min_support=MIN_SUPPORT,
        use_colnames=True
    )

    print(f"[RESULT] FP-Growth:")
    print(f"  Timp executie: {round(t_fp, 2)} secunde")
    print(f"  Itemset-uri frecvente: {len(freq_fp)}")

    # =========================
    # 5. Apriori
    # =========================
    print("\n[INFO] Rulare Apriori...")
    try:
        t_ap, freq_ap = timed(
            apriori,
            basket,
            min_support=MIN_SUPPORT,
            use_colnames=True
        )

        print(f"[RESULT] Apriori:")
        print(f"  Timp executie: {round(t_ap, 2)} secunde")
        print(f"  Itemset-uri frecvente: {len(freq_ap)}")

        # =========================
        # 6. Comparatie
        # =========================
        if t_fp < t_ap:
            print(
                f"\n[INFO] FP-Growth a fost de aproximativ "
                f"{round(t_ap / t_fp, 2)} ori mai rapid decat Apriori"
            )
        else:
            print(
                f"\n[INFO] Apriori a fost de aproximativ "
                f"{round(t_fp / t_ap, 2)} ori mai rapid decat FP-Growth"
            )

    except MemoryError:
        print("[WARN] Apriori a esuat din cauza memoriei.")
    except KeyboardInterrupt:
        print("[WARN] Apriori a fost oprit manual (timp mare de rulare).")


if __name__ == "__main__":
    main()
