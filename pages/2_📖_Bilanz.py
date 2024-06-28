import streamlit as st
import pandas as pd
import altair as alt
from streamlit import session_state as ss

st.set_page_config(page_title="Contracta", page_icon=":bar_chart:", layout="centered")

# Check Login Status

if not st.session_state.get('authentication_status', False):
    st.info('Bitte anmelden auf der Login Seite')
    st.stop()


st.title("Bilanz")
st.markdown(
        """Auf dieser Seite finden Sie alle relevanten Kennzahlen zu Ihrer Bilanz im Verlauf der Zeit."""
    )

# Define the data as a dictionary with the columns for each year and the respective values, including empty cells as None
bilanz_umsatz = {
    'Jahr': ['2019', '2020', '2021', '2022'],
    'Umsatz': [1782204, 922579, 1619811, 2118751],
    'Umsatz pro Zimmer': [59746, 30456, 63452, 66789],
    'Umsatz pro Nächtigung': [122, 78, 125, 131],
    'EBITDA': [423567, 212345, 498765, 532478],
    'EBITDA pro Zimmer': [32365, 30456, 63452, 66789],
    'EBITDA pro Nächtigung': [21, 15, 25, 33],
    'Bilanzgewinn': [86754, -20324, 91329, 101788],
    'Bilanzgewinn pro Zimmer': [1056, -854, 1345, 1532],
    'Bilanzgewinn pro Nächtigung': [16.4, -3.4, 17.2, 18.7],
}

bilanz_umsatz = pd.DataFrame(bilanz_umsatz)

# Transpose the DataFrame
bilanz_umsatz = bilanz_umsatz.set_index('Jahr').T

# Function to format numbers with custom thousands and decimal separators
def format_numbers(x):
    if isinstance(x, float) and not x.is_integer():
        formatted = f"{x:,.2f}"  # Format float with comma as thousands separator and dot as decimal separator
    else:
        formatted = f"{x:,.0f}"  # Format integer with comma as thousands separator
    # Replace comma with dot for thousands and dot with comma for decimals
    formatted = formatted.replace(',', 'X').replace('.', ',').replace('X', '.')
    # Prefix each number with the Euro sign
    return f"€{formatted}"

# Apply number formatting
styled_df = bilanz_umsatz.style.format(format_numbers)

st.subheader('Einnahmen')
st.dataframe(styled_df, use_container_width=True)



st.subheader('Ausgaben')


ausgaben = {
    'Jahr': ['2019', '2020', '2021', '2022'],
    'Wareneinsatz': [241534, 142367, 235489, 270897],
    'Wareneinsatz pro Zimmer': [2893, 1453, 3123, 2322],
    'Wareneinsatz pro Nächtigung': [15.4, 8.9, 16.3, 17.9],
    'Personal': [545637, 340678, 533789, 576890],
    'Personal pro Zimmer': [1123, 789, 1345, 1675],
    'Personal pro Nächtigung': [6.5, 4.3, 7.9, 8.2],
    'Marketing': [71892, 23456, 76880, 81900],
    'Marketing pro Zimmer': [340, 112, 423, 510],
    'Marketing pro Nächtigung': [3.4, 1.8, 5.1, 4.5],
    'Energie': [47568, 28900, 53490, 55900],
    'Energie pro Zimmer': [180, 75, 234, 287],
    'Energie pro Nächtigung': [2.3, 1.5, 2.7, 3.1]
}

ausgaben = pd.DataFrame(ausgaben)

# Transpose the DataFrame
ausgaben = ausgaben.set_index('Jahr').T

styled_df_ausgaben = ausgaben.style.format(format_numbers)
st.dataframe(styled_df_ausgaben, use_container_width=True)


st.markdown("<div style='margin: 25px;'></div>", unsafe_allow_html=True)
st.subheader('Bilanzposten im Verlauf der Zeit')

# Create three columns
posten1, posten2 = st.columns(2)
# Place each widget in its respective column
with posten1:
    p1 = st.selectbox(
"Wählen Sie den ersten Bilanzposten",
("Anlagevermögen", "Umlaufvermögen", "Eigenkapital", "Fremdkapital", "Kassa", "Forderungen", "Verbindlichkeiten"),
index=0,
placeholder="",
)
with posten2:
    p2 = st.selectbox(
"Wählen Sie den zweiten Bilanzposten",
("Anlagevermögen", "Umlaufvermögen", "Eigenkapital", "Fremdkapital", "Kassa", "Forderungen", "Verbindlichkeiten"),
index=1,
placeholder="",
)

bilanz = {
    'Jahr': ['2019', '2020', '2021', '2022'],
    'Anlagevermögen': [867000, 756432, 854982, 912345],
    'Umlaufvermögen': [734901, 654981, 745632, 765900],
    'Eigenkapital': [802345, 768900, 823546, 867900],
    'Fremdkapital': [735000, 699800, 756899, 777777],
    'Kassa': [80432, 56900, 90321, 101234],
    'Forderungen': [23000, 34560, 29012, 19076],
    'Verbindlichkeiten': [80900, 123432, 110987, 99087]
}

bilanz = pd.DataFrame(bilanz)


# Function to create a line chart for two selected variables
def create_line_chart(df, year_col, value_cols):
    # Transform DataFrame to long format for easier plotting with Altair
    long_df = df.melt(id_vars=[year_col], value_vars=value_cols, var_name='Kategorie', value_name='Wert')

    # Create the chart
    base_chart = alt.Chart(long_df).encode(
        x=alt.X(f"{year_col}:O", title='Jahr'),
        y=alt.Y('Wert:Q', title='€', scale=alt.Scale(zero=False)),
        color=alt.Color('Kategorie:N', legend=alt.Legend(title='Kategorie', orient='bottom'))
    ).properties(
        height=400,
        title=f"Vergleich von {value_cols[0]} und {value_cols[1]}"
    )

    # Define the line part of the chart
    line_chart = base_chart.mark_line(point=True).encode(
        size=alt.value(3)  # Line thickness
    )

    # Define the point part of the chart
    point_chart = base_chart.mark_point(filled=True, size=100).encode(
        tooltip=[alt.Tooltip('Kategorie:N', title='Kategorie'), alt.Tooltip('Wert:Q', title='Wert', format=',')]
    )

    # Define the text part of the chart
    text_chart = base_chart.mark_text(
        align='center',
        dy=-15,  # Nudge text up so it doesn't overlap with the points
        fontWeight='bold'
    ).encode(
        text=alt.Text('Wert:Q', format=',')
    )

    # Layer the text marks on top of the bar chart
    final_chart = (line_chart + point_chart + text_chart)

    return final_chart

# Display the chart if two different posts are selected
if p1 != p2:
    st.altair_chart(create_line_chart(bilanz, 'Jahr', [p1, p2]), use_container_width=True)
else:
    st.error("Bitte wählen Sie zwei verschiedene Posten.")
