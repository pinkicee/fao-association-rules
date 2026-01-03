import pandas as pd
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import fpgrowth, apriori

from config import *
from utils import ensure_dirs, load_merged_df, build_transactions, filter_rare_items, timed


def main():
    ensure_dirs()
    df = load_merged_df()

    transactions = build_transactions(df)
    transactions, kept = filter_rare_items(
        transactions, RARE_ITEM_SUPPORT_THRESHOLD
    )

    te = TransactionEncoder()
    basket = pd.DataFrame(
        te.fit(transactions).transform(transactions),
        columns=te.columns_,
        dtype=bool
    )

    t_fp, freq_fp = timed(
        fpgrowth, basket, min_support=MIN_SUPPORT, use_colnames=True
    )

    try:
        t_ap, freq_ap = timed(
            apriori, basket, min_support=MIN_SUPPORT, use_colnames=True
        )
        print("FP-Growth:", round(t_fp, 2), "sec")
        print("Apriori:", round(t_ap, 2), "sec")
    except:
        print("Apriori nu a rulat din motive de resurse.")


if __name__ == "__main__":
    main()