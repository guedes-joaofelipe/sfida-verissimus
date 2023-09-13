import pandas as pd

SHEET_ID = "1ZST9mROwpwAwRC95riuN7-FNOMfC-3UEmifGVrPCXE8"
SHEET_NAME = "Coniugazione"


def get_conjugation(form="Infinitivo"):
    url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={SHEET_NAME}"
    df = pd.read_csv(url)

    return df
