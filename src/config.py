from pathlib import Path

# Cai proiect
PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data"
RAW_DIR = DATA_DIR / "raw"
PROCESSED_DIR = DATA_DIR / "processed"

# Fisiere
CONSUMPTION_CSV = RAW_DIR / "consumption_user.csv"
SUBJECT_CSV = RAW_DIR / "subject_user.csv"

# Parametri mining
MIN_SUPPORT = 0.03
MIN_CONFIDENCE = 0.40
MIN_LIFT = 1.20

# Limitari reguli
MAX_ANTECEDENT_LEN = 2
CONSEQUENT_LEN = 1

# Prag eliminare itemi rari
RARE_ITEM_SUPPORT_THRESHOLD = 0.05
