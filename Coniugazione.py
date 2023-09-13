import os
import sys
import pandas as pd
import numpy as np
import streamlit as st
from utils import database as db


def display_filters(df_verbs: pd.DataFrame):
    filter_columns = st.columns(3)

    with filter_columns[0]:
        options = sorted(df_verbs["Coniugazione"].unique())

        st.multiselect(
            "Coniugazione",
            options=options,
            key="coniugazione",
            default=options
            # disabled=not st.session_state.force_alternative,
        )

    with filter_columns[1]:
        options = sorted(df_verbs["Regolari"].unique())

        st.multiselect(
            "Regolari",
            options=options,
            key="regolari",
            default=options
            # disabled=not st.session_state.force_alternative,
        )

    with filter_columns[2]:
        options = sorted(df_verbs["Verbo"].unique())

        st.multiselect(label="Verbo", options=options, key="verbo")


def get_filtered_verbs(df_verbs: pd.DataFrame):
    df = df_verbs.copy()
    if len(st.session_state.coniugazione) > 0:
        df = df[df["Coniugazione"].isin(st.session_state.coniugazione)]

    if len(st.session_state.regolari) > 0:
        df = df[df["Regolari"].isin(st.session_state.regolari)]

    if len(st.session_state.verbo) > 0:
        df = df[df["Verbo"].isin(st.session_state.verbo)]

    return df


def display_exercise(df: pd.DataFrame):
    exercise = df.sample()

    st.session_state.pronome = np.random.choice(
        ["Io", "Tu", "Lei", "Noi", "Voi", "Loro"]
    )
    verb = exercise["Verbo"].to_numpy()[0]
    st.session_state.correct_answer = exercise[st.session_state.pronome].to_numpy()[0]

    st.text_input(
        label=f"**{verb.title()}**",
        key="user_answer",
        placeholder=st.session_state.pronome,
        on_change=check_answer(),
    )

    return st.session_state.correct_answer


def check_answer():
    if st.session_state.user_answer != "":
        if (
            st.session_state.correct_answer.lower().strip()
            == st.session_state.user_answer.lower().strip()
        ):
            st.success(
                f"Correcto! **{st.session_state.pronome} {st.session_state.user_answer}**"
            )
        else:
            st.info("Risposta: " + st.session_state.user_answer)
            st.error(f"L'opzione giusta è **{st.session_state.correct_answer}**")


def reset_answers():
    for variable in ["user_answer", "correct_answer", "pronome"]:
        if variable not in st.session_state:
            st.session_state[variable] = ""


def main():
    st.set_page_config(
        layout="wide",
        page_title="Sfida Verissimus :it:",
        page_icon=":it:",
        initial_sidebar_state="collapsed",
    )

    st.sidebar.header("Sfida Verissimus :it:")
    st.header("Coniugazione")
    st.subheader("Coniuga il verbo en italiano :it:")

    df_verbs = db.get_conjugation(form="Infinitivo")

    reset_answers()
    display_filters(df_verbs)
    df_verbs_filtered = get_filtered_verbs(df_verbs)

    if st.session_state.user_answer == "":
        display_exercise(df_verbs_filtered)
    else:
        check_answer()
        if st.button("Prossimo"):
            reset_answers()

    st.markdown("-----")
    if st.checkbox("Mostrare dati", value=False, key="show_data"):
        st.dataframe(df_verbs_filtered)


if __name__ == "__main__":
    main()
