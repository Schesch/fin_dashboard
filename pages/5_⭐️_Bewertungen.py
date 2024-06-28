import streamlit as st
import pandas as pd
from streamlit import session_state as ss

st.set_page_config(page_title="Contracta", page_icon=":bar_chart:", layout="centered")

# Check Login Status

if not st.session_state.get('authentication_status', False):
    st.info('Bitte anmelden auf der Login Seite')
    st.stop()

file_path = file_path = 'https://raw.githubusercontent.com/Schesch/accounting_dashboard/main/hotel_list.xlsx'
df_rating = pd.read_excel(file_path)



st.title("Google Bewertungen")
st.markdown(
        """Auf dieser Seite finden Sie Ihre Google Bewertung und können diese mit anderen Südtiroler Hotels vergleichen."""
    )

#### DEFINE FUNCTION FOR METRIC STYLE
def style_metric_cards(
    background_color: str = "#f7ddc3",
    border_size_px: int = 2,
    border_color: str = "#000000",
    border_radius_px: int = 10,
) -> None:
    st.markdown(
        f"""
        <style>
            div[data-testid="stMetric"],
            div[data-testid="metric-container"] {{
                text-align: center;
                background-color: {background_color};
                border: {border_size_px}px solid {border_color};
                padding: 5% 5% 5% 10%;
                border-radius: {border_radius_px}px;
            }}
        </style>
        """,
        unsafe_allow_html=True,
    )

col1, col2 = st.columns(2)
col1.metric("Google Bewertung", "4.7 ⭐️")
col2.metric("Anzahl Bewertungen", "346")


st.markdown("<div style='margin: 50px;'></div>", unsafe_allow_html=True)

st.write(
        """Vergleichen Sie sich mit über 100 anderen Südtiroler Hotels je nach Bezirk und Sterne."""
    )

st.markdown("<div style='margin: 25px;'></div>", unsafe_allow_html=True)


v1, v2 = st.columns(2)
# Place each widget in its respective column
with v1:
    parameter1 = st.selectbox(
"Wählen Sie den Bezirk",
("Burggrafenamt", "Vinschgau", "Pustertal", "Salten-Schlern", "Überetsch-Unterland"),
index=0,
placeholder="",
)
with v2:
    parameter2 = st.selectbox(
"Wählen Sie die Sterne der Hotels",
(3, 4, 5),
index=0,
placeholder="",
)

# Filtering the DataFrame based on user input
filtered_df = df_rating[(df_rating['Bezirk'] == parameter1) & (df_rating['Sterne'] == parameter2)]

# Calculate the mean rating for the filtered DataFrame
mean_rating = filtered_df['rating'].mean()
mean_n = filtered_df['n_rating'].mean()

st.markdown("<div style='margin: 25px;'></div>", unsafe_allow_html=True)

if not filtered_df.empty:
    vg1, vg2 = st.columns(2)
    vg1.metric("Durchschnittliche Google Bewertung", f"{mean_rating:.1f} ⭐️")
    vg2.metric("Durchschnittliche Anzahl Bewertungen", f"{mean_n:.0f}")
else:
    st.write("Keine Daten vorhanden für ausgewählte Parameter.")
