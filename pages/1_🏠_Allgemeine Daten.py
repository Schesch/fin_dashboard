import streamlit as st
import pandas as pd
import altair as alt
from streamlit import session_state as ss

st.set_page_config(page_title="Contracta", page_icon=":bar_chart:", layout="centered")

# Check Login Status

if not st.session_state.get('authentication_status', False):
    st.info('Bitte anmelden auf der Login Seite')
    st.stop()


# Data from the image
df1 = {
    'Jahr': ["2019", "2020", "2021", "2022"],
    'Sterne': ["4", "4", "4", "4S"],  # Revenue
    'Betten': ["78", "78", "78", "84"],
    'Nächtigungen': ["14.075", "6.312", "16.783", "19.823"],
    'Zimmer': ["30", "30", "30", "32"],
    'Bruttoauslastung (%)': ["51,3", "28,2", "53,5", "59,7"],
    'Auslastung IDM (%)': ["63,9", "39,5", "67,3", "72,3"]
}

df1 = pd.DataFrame(df1)

st.title("Allgemeine Daten")
st.markdown("<div style='margin: 25px;'></div>", unsafe_allow_html=True)
st.subheader("Kennzahlen zu Ihrem Hotel")

# Set 'Jahr' as index
df1.set_index('Jahr', inplace=True)

# Display the DataFrame as a table
st.dataframe(df1, use_container_width=True)
# Adding a caption below the table
st.caption("Die Kennzahlen sind auf 365 Tage berechnet")




df2 = {
    'Jahr': ["2019", "2020", "2021", "2022"],
    'Nächtigungen': ["14.075", "6.312", "16.783", "19.823"],
    'Interner Benchmark' : ["17.032", "9.985", "20.234", "22.455"]
}

df3 = {
    'Jahr': ["2019", "2020", "2021", "2022"],
    'Bruttoauslastung (%)': ["51,3", "28,2", "53,5", "59,7"],
    'Auslastung IDM (%)': ["63,9", "39,5", "67,3", "72,3"]
}

df2 = pd.DataFrame(df2)
df3 = pd.DataFrame(df3)

# Convert the number strings to actual numbers
df2['Nächtigungen'] = df2['Nächtigungen'].str.replace('.', '').astype(int)
df2['Interner Benchmark'] = df2['Interner Benchmark'].str.replace('.', '').astype(int)
df3['Bruttoauslastung (%)'] = df3['Bruttoauslastung (%)'].str.replace(',', '.').astype(float)
df3['Auslastung IDM (%)'] = df3['Auslastung IDM (%)'].str.replace(',', '.').astype(float)

df_long2 = df2.melt('Jahr', var_name='Kategorie', value_name='Wert')
df_long3 = df3.melt('Jahr', var_name='Kategorie', value_name='Wert')

# Define the function to create a line chart with points and value labels
def create_line_chart(df, year_col, value_col, category_col, value_title, plot_title):
    # Determine the min and max for the y-axis
    min_value = df[value_col].min() - (df[value_col].min() % 10)  # Floor to nearest 10
    max_value = df[value_col].max() + (10 - df[value_col].max() % 10)  # Ceil to nearest 10

    base_chart = alt.Chart(df).encode(
        x=alt.X(f"{year_col}:O", axis=alt.Axis(title=year_col)),
        y=alt.Y(f"{value_col}:Q", axis=alt.Axis(title=value_title), 
                scale=alt.Scale(domain=[min_value, max_value])),
        color=alt.Color(f"{category_col}:N", legend=alt.Legend(title='Kategorien', orient='bottom')),
    ).properties(
        height=450,
        title=plot_title
    )

    line_chart = base_chart.mark_line(point=True).encode(
        size=alt.value(3)
    )

    point_chart = base_chart.mark_point(filled=True, size=100).encode(
        tooltip=[f"{year_col}:O", f"{category_col}:N", f"{value_col}:Q"]
    )

    text_chart = base_chart.mark_text(
        align='center',
        dy=-15,  # Nudge text up so it doesn't overlap with the points
        fontWeight='bold'
    ).encode(
        text=alt.Text(f"{value_col}:Q", format=',')
    )

    final_chart = line_chart + point_chart + text_chart

    return final_chart

# Display charts in Streamlit
st.markdown("<div style='margin: 50px;'></div>", unsafe_allow_html=True)
st.altair_chart(create_line_chart(df_long2, 'Jahr', 'Wert', 'Kategorie', 'Anzahl Nächtigungen', 'Nächtigungen pro Jahr'), use_container_width=True)
st.markdown("<div style='margin: 50px;'></div>", unsafe_allow_html=True)
st.altair_chart(create_line_chart(df_long3, 'Jahr', 'Wert', 'Kategorie', 'Auslastung in %', 'Bruttoauslastung auf 365 Tage'), use_container_width=True)
