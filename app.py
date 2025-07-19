import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="CashFlow App", layout="wide")
st.title("📊 CashFlow – analiza wydatków")

@st.cache_data
def load_data():
    df = pd.read_csv("glide_expenses_clean.csv")
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df["month"] = df["month"].astype(str)
    return df

df = load_data()

available_months = sorted(df["month"].dropna().unique())
selected_month = st.selectbox("Wybierz miesiąc", available_months)

filtered_df = df[df["month"] == selected_month]

total = filtered_df["amount"].sum()
st.metric("💸 Suma wydatków", f"{total:,.2f} zł")

st.subheader("📋 Lista wydatków")
st.dataframe(filtered_df[["date", "description", "category", "amount"]].sort_values("date"))

st.subheader("📈 Wydatki według kategorii")
category_summary = filtered_df.groupby("category")["amount"].sum().sort_values()

fig, ax = plt.subplots(figsize=(8, 5))
category_summary.plot(kind="barh", ax=ax, color="#3399cc")
ax.set_xlabel("Kwota (zł)")
ax.set_ylabel("Kategoria")
ax.set_title("Wydatki wg kategorii")
st.pyplot(fig)
