import streamlit as st
import pandas as pd
import altair as alt
from streamlit import session_state as ss

st.set_page_config(page_title="Contracta", page_icon=":bar_chart:", layout="centered")

# Check Login Status

if not st.session_state.get('authentication_status', False):
    st.info('Bitte anmelden auf der Login Seite')
    st.stop()


st.title("Liquidität und Zahlungsfähigkeit")
st.markdown("Die Current Ratio ist eine Liquiditätskennzahl , die die Fähigkeit eines Unternehmens misst, kurzfristige oder innerhalb eines Jahres fällige Verbindlichkeiten zu begleichen. Sie wird folgendermaßen berechnet:")
st.latex(r'''
    \text{Current Ratio} = 
    \frac{\text{Umlaufvermögen}}{\text{Kurzfristige Verbindlichkeiten}}
''')

df1 = {
    'Jahr': [2019, 2020, 2021, 2022],
    'Current Ratio': [0.06, 0.21, 0.35, 0.53],
    'Benchmark': [0.75, 0.90, 1.30, 1.40]
}

df2 = {
    'Jahr': [2019, 2020, 2021, 2022],
    'VBK/Umsatz': [1.03, 1.26, 1.65, 1.50],
    'Benchmark': [1.33, 1.43, 1.92, 1.87]
}

df1 = pd.DataFrame(df1)
df2 = pd.DataFrame(df2)

df_long1 = df1.melt('Jahr', var_name='Category', value_name='Value')
df_long2 = df2.melt('Jahr', var_name='Category', value_name='Value')




def create_line_chart(df, year_col, value_col, category_col, target_range, value_title, plot_title):
    df[year_col] = df[year_col].astype(int)

    # Create line and point charts for each category
    lines_points = alt.Chart(df).mark_line(point=True).encode(
        x=alt.X(f"{year_col}:N", scale=alt.Scale(domain=df[year_col].unique().tolist()), axis=alt.Axis(title=year_col)),
        y=alt.Y(f"{value_col}:Q", axis=alt.Axis(title=value_title)),
        color=alt.Color(f"{category_col}:N", legend=alt.Legend(title='Categories', orient='bottom')),
        tooltip=[f"{year_col}:N", f"{category_col}:N", alt.Tooltip(f"{value_col}:Q", format=',')]
    )

    # Create text labels for the points
    text_labels = lines_points.mark_text(
        align='center',
        dy=-15,  # Adjust text position above the points
        fontWeight='bold'
    ).encode(
        text=alt.Text(f"{value_col}:Q", format=',.2f')
    )



# Create the 'Zielbereich' area chart
    target_area = alt.Chart(target_range).mark_area(opacity=0.3, color='lightgreen').encode(
        x=alt.X(f"{year_col}:N", axis=alt.Axis(title=year_col)),
        y=alt.Y('lower:Q'),
        y2='upper:Q'
    )

    # Add text label for the 'Zielbereich'
    target_label = alt.Chart(target_range).mark_text(
        align='center',
        baseline='bottom',
        dy=10,  # Adjust the vertical position to be slightly above the area
        dx = 50,
        color='green',  # Adjust text color as needed
        size=11  # Adjust text size as needed
    ).encode(
        x=alt.X(f'mean({year_col}):O'),  # Center the text in the middle of the chart
        y=alt.Y('mean(upper):Q'),  # Position the text based on the average of the upper bounds
        text=alt.value('Zielbereich')  # The text to display
    )


    final_chart = alt.layer(
    lines_points, text_labels, target_area, target_label
).properties(
    height=450,
    title=plot_title
)

    return final_chart

# Example usage
# Create the DataFrame for the target range with explicit 'Year' column
target_range1 = pd.DataFrame({
    'Jahr': [2019, 2020, 2021, 2022],
    'lower': [0.8, 0.8, 0.8, 0.8],
    'upper': [1.2, 1.2, 1.2, 1.2],
    'Zielbereich' : ['', '', '', '']
})

target_range2 = pd.DataFrame({
    'Jahr': [2019, 2020, 2021, 2022],
    'lower': [1.3, 1.3, 1.3, 1.3],
    'upper': [1.8, 1.8, 1.8, 1.8],
    'Zielbereich' : ['', '', '', '']
})

# Call the function
st.markdown("<div style='margin: 25px;'></div>", unsafe_allow_html=True)
plot1 = create_line_chart(df_long1, 'Jahr', 'Value', 'Category', target_range1, '%', 'Current Ratio')
st.markdown("<div style='margin: 25px;'></div>", unsafe_allow_html=True)
plot2 = create_line_chart(df_long2, 'Jahr', 'Value', 'Category', target_range2, '%', 'Verbindlichkeiten / Umsatz')

# Display the chart in Streamlit
st.altair_chart(plot1, use_container_width=True)
st.altair_chart(plot2, use_container_width=True)
