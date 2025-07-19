
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# --- Konfiguracja strony ---
st.set_page_config(page_title="Budżet 2025", layout="wide")

st.title("📊 Aplikacja Budżetowa 2025")

# --- Wczytanie danych ---
@st.cache_data
def load_data():
    xls = pd.ExcelFile("Budżed_2025_shared 2 2.xlsm", engine="openpyxl")
    
    wydatki = pd.read_excel(xls, sheet_name="Wydatki", header=1)
    wydatki = wydatki.dropna(subset=["Kwota", "Za Co", "Kategoria", "Data", "Miesiąc"])
    wydatki["Data"] = pd.to_datetime(wydatki["Data"])
    wydatki["Kwota"] = pd.to_numeric(wydatki["Kwota"], errors="coerce")

    wplywy = pd.read_excel(xls, sheet_name="Wpływy", header=0)
    wplywy = wplywy.dropna(subset=["Kwota", "Revenue", "Data", "Miesiąc"])
    wplywy["Data"] = pd.to_datetime(wplywy["Data"])
    wplywy["Kwota"] = pd.to_numeric(wplywy["Kwota"], errors="coerce")

    return wydatki, wplywy

wydatki, wplywy = load_data()

# --- Agregacja miesięczna ---
suma_wydatkow = wydatki.groupby("Miesiąc")["Kwota"].sum().rename("Suma Wydatków")
suma_wplywow = wplywy.groupby("Miesiąc")["Kwota"].sum().rename("Suma Wpływów")

budzet = pd.concat([suma_wplywow, suma_wydatkow], axis=1).fillna(0)
budzet["Bilans"] = budzet["Suma Wpływów"] - budzet["Suma Wydatków"]
budzet.reset_index(inplace=True)

# --- Interfejs użytkownika ---
st.subheader("📅 Podsumowanie miesięczne")
st.dataframe(budzet.style.format({"Suma Wpływów": "{:,.2f} zł", "Suma Wydatków": "{:,.2f} zł", "Bilans": "{:,.2f} zł"}))

# --- Wykres ---
st.subheader("📈 Wykres bilansu miesięcznego")
fig, ax = plt.subplots(figsize=(10, 4))
ax.bar(budzet["Miesiąc"], budzet["Bilans"], color=["green" if x >= 0 else "red" for x in budzet["Bilans"]])
ax.axhline(0, color="black", linewidth=0.8)
ax.set_ylabel("Bilans (zł)")
ax.set_xlabel("Miesiąc")
ax.set_title("Bilans miesięczny")
st.pyplot(fig)
