from utils import ensure_dirs, load_merged_df
from config import PROCESSED_DIR


def main():
    ensure_dirs()
    df = load_merged_df()

    # Tranzactii pentru EDA
    transactions = (
        df.groupby(["SUBJECT", "SURVEY_DAY", "ADM0_NAME"])["INGREDIENT"]
        .apply(lambda x: sorted(set(x)))
        .reset_index(name="items")
    )

    transactions["length"] = transactions["items"].apply(len)

    print("Nr tranzactii:", len(transactions))
    print("Nr subiecti:", df["SUBJECT"].nunique())
    print("Nr tari:", df["ADM0_NAME"].nunique())
    print("Nr ingrediente unice:", df["INGREDIENT"].nunique())
    print(transactions["length"].describe())

    # Salveaza rezultate
    transactions.to_csv(PROCESSED_DIR / "transactions_eda.csv", index=False)


if __name__ == "__main__":
    main()