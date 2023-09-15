import pandas as pd


def get_conjugation(form="Indicativo"):
    SHEET_ID = "1ZST9mROwpwAwRC95riuN7-FNOMfC-3UEmifGVrPCXE8"
    SHEET_NAME = "Coniugazione"
    url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={SHEET_NAME}"
    df = pd.read_csv(url)

    return df


def get_numbers():
    SHEET_ID = "2PACX-1vQs-_bnOUFveo2YMY5IKMT5c6uLuflq86mTz0hxqc9Vyp1_VPsf0cR8B2HUu2xt2h2A0Wfh_7r6iEET"
    SHEET_NAME = "Numeri"
    url = f"https://docs.google.com/spreadsheets/d/e/{SHEET_ID}/pub?output=csv"
    df = pd.read_csv(url)

    return df
