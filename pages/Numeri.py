import os
import sys
import pandas as pd
import numpy as np
import streamlit as st
from utils import database as db


def display_filters(df: pd.DataFrame):
    if st.checkbox("Filtrare numeri", value=False, key="filter_numeri"):
        filter_columns = st.columns(3)

        with filter_columns[0]:
            st.slider(
                "Range", min_value=0, max_value=100, step=1, key="range", value=(0, 100)
            )


def get_filtered_verbs(df: pd.DataFrame):
    if st.session_state.filter_numeri:
        df = df[df["Numero"] >= st.session_state.range[0]]
        df = df[df["Numero"] <= st.session_state.range[1]]

    return df


def display_exercise(df: pd.DataFrame):
    exercise = df.sample()

    numero = exercise["Numero"].to_numpy()[0]
    st.session_state.correct_answer = exercise["Scrittura"].to_numpy()[0]

    st.markdown(f"## {numero}")
    st.text_input(
        label=str(numero),
        key="user_answer",
        placeholder="Scrittura",
        on_change=check_answer(),
        label_visibility="collapsed",
    )

    return st.session_state.correct_answer


def check_answer():
    if st.session_state.user_answer != "":
        if (
            st.session_state.correct_answer.lower().strip()
            == st.session_state.user_answer.lower().strip()
        ):
            st.success(f"Correcto! **{st.session_state.user_answer}**")
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
    st.header("Numeri")
    st.subheader("Scrivi i numeri en italiano :it:")

    df_numeri = db.get_numbers()

    reset_answers()
    display_filters(df_numeri)
    df_numeri_filtered = get_filtered_verbs(df_numeri)

    if st.session_state.user_answer == "":
        display_exercise(df_numeri_filtered)
    else:
        check_answer()
        if st.button("Prossimo"):
            reset_answers()

    st.markdown("-----")
    if st.checkbox("Mostrare dati", value=False, key="show_data"):
        st.dataframe(df_numeri_filtered)


if __name__ == "__main__":
    main()
