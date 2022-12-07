# import the required libraries
import datetime
import json
import matplotlib.pyplot as plt
import pandas as pd
import requests
import seaborn as sns
import streamlit as st

st.set_page_config(layout = "wide")

# change CSS for h1 and h3
st.markdown(
    """
        <style>
            h1 {
                text-align: center;
                color: grey
            }
            h3 {
                text-align: center;
                color: grey
            }
        </style>
    """,
    unsafe_allow_html = True)

# load data using caching mechanism
@st.cache
def load_data_cases():
    data_covid_cases = (
        pd
            .read_csv("CovidFaelle_Timeline.csv",
                      delimiter = ";",
                      decimal=",",
                      parse_dates = ["Time"],
                      index_col = "Time",
                      dayfirst = True
                      )
            .filter(["Bundesland", "SiebenTageInzidenzFaelle"])
        )
    return data_covid_cases

@st.cache
def load_data_age():
    data_covid_cases_age = (
        pd
            .read_csv("CovidFaelle_Altersgruppe.csv",
                      delimiter = ";",
                      parse_dates = ["Time"],
                      index_col = "Time",
                      dayfirst = True
                      )
            .filter(["Altersgruppe", "Bundesland", "Geschlecht", "AnzahlTot"])
        )
    return data_covid_cases_age

data_covid_cases = load_data_cases()
data_covid_cases_age = load_data_age()

# Jahre für Radio-Buttons ermitteln
years = data_covid_cases.index.year.unique()
# Bundesländer für Drop-Down ermitteln
states = data_covid_cases["Bundesland"].unique()

# sidebar setup
st.sidebar.title("Filter")
year = st.sidebar.radio("Jahr:",
                        years)
date = st.sidebar.date_input("Datum:",
                             value = max(data_covid_cases.loc[str(year)].index),
                             min_value = min(data_covid_cases.loc[str(year)].index),
                             max_value = max(data_covid_cases.loc[str(year)].index))
state = st.sidebar.selectbox("Bundesland:",
                             states)
with st.sidebar.form(key = "myForm",
                     clear_on_submit = True):
    address = st.text_input("Adresse eingeben:")
    submit_button = st.form_submit_button("Suchen")
geo = st.sidebar.empty()
#geo.text("Geolocation: ")

# Geoloction ermitteln
if submit_button:
    res = requests.get(url = "http://geolocation:8000/geolocation?address='" + str(address) + "'") #127.0.0.1, localhost, 0.0.0.0, 0.0.0.0
    geo.text("Geolocation von " + address + ": " + res.text)

# add a title and intro text
st.title("Covid19-Dashboard")

# Daten entsprechend der Einstellungen filtern
data_covid_cases = data_covid_cases[data_covid_cases["Bundesland"] == state].loc[str(year)]
data_covid_cases_age = data_covid_cases_age[data_covid_cases_age["Bundesland"] == state].loc[str(date.strftime("%m.%d.%Y"))]

st.subheader("Entwicklung der 7-Tages-Inzidenz für " + state + " im Jahr " + str(year))

fig, ax = plt.subplots(1, 1)
ax.plot(data_covid_cases["SiebenTageInzidenzFaelle"])
ax.set_xlabel("Zeit")
ax.set_ylabel("7-Tages-Inzidenz")
plt.xticks(rotation = 45)

st.pyplot(fig)

st.subheader("kumulierte Todesfälle nach Altersgruppe für " + state + " (Stand: " + str(date.strftime("%d.%m.%Y")) + ")")

order = ["<5", "5-14", "15-24", "25-34", "35-44", "45-54", "55-64", "65-74", "75-84", ">84"]

fig, ax = plt.subplots(1, 1)
ax = sns.barplot(data = data_covid_cases_age,
                 x = "Altersgruppe",
                 y = "AnzahlTot",
                 hue = "Geschlecht",
                 order = order,
                 ci = None)
ax.set_xlabel("Altersgruppe")
ax.set_ylabel("Anzahl Tote")

st.pyplot(fig)