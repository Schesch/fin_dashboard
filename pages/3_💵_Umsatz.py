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
    'Year': [2019, 2020, 2021, 2022],
    'Umsatz': [1782204, 922579, 1619811, 2118751],  # Revenue
    'EBITDA': [420640, 202608, 699207, 781716]  # Earnings Before Interest, Taxes, Depreciation, and Amortization
}

df2 = {
    'Year': [2019, 2020, 2021, 2022],
    'Wareneinsatz': [13, 12, 15, 18],  # Revenue
    'Personal': [32, 31, 36, 38]  # Earnings Before Interest, Taxes, Depreciation, and Amortization
}

# Create DataFrame
df1 = pd.DataFrame(df1)
df2 = pd.DataFrame(df2)


st.title("Umsatz")
st.markdown("Aktuelle Kennzahlen zu Ihrem Umsatz")

# Convert DataFrame from wide to long format
df_long1 = df1.melt('Year', var_name='Category', value_name='Value')
df_long2 = df2.melt('Year', var_name='Category', value_name='Value')

def create_grouped_bar_chart(df, year_col, value_col, category_col, value_title='€', plot_title="Grouped Bar Chart"):
    # Create the Altair chart with dynamic axis properties and data columns
    chart = alt.Chart(df).mark_bar().encode(
        x=alt.X(f"{year_col}:N", axis=alt.Axis(labelColor='black', titleColor='black', title=year_col)),
        y=alt.Y(f"{value_col}:Q", axis=alt.Axis(title=value_title, labelColor='black', titleColor='black')),
        xOffset=f"{category_col}:N",
        color=alt.Color(f"{category_col}:N", legend=alt.Legend(title='Categories', orient='bottom'))  # Adjust the legend
    ).properties(
        height=450,  # Setting the height of the plot
        title=plot_title  # Setting the title of the plot
    )

    # Create text marks to display values above each bar with formatting
    text_chart = chart.mark_text(
        align='center',
        baseline='bottom',
        dy=-5  # Nudge the text up so it doesn't overlap with the top of the bar
    ).encode(
        text=alt.Text(f"{value_col}:Q", format=',')  # Apply thousands separator
    )

    # Layer the text marks on top of the bar chart
    final_chart = (chart + text_chart)

    # Display the chart in Streamlit
    st.altair_chart(final_chart, use_container_width=True)

create_grouped_bar_chart(df_long1, 'Year', 'Value', 'Category', '€', 'Umsatz & EBITDA')

st.markdown("<div style='margin: 25px;'></div>", unsafe_allow_html=True) 

create_grouped_bar_chart(df_long2, 'Year', 'Value', 'Category', '%', 'Wareneinsatz & Personal zu Umsatz')



df3 = {
    'Year': [2019, 2020, 2021, 2022],
    'Umsatz': [25000, 22345, 28754, 31467],  # Revenue
    'EBITDA': [18756, 16453, 19875, 20500]  # Earnings Before Interest, Taxes, Depreciation, and Amortization
}

df4 = {
    'Year': [2019, 2020, 2021, 2022],
    'Umsatz': [235, 195, 256, 310],  # Revenue
    'EBITDA': [180, 165, 192, 200]  # Earnings Before Interest, Taxes, Depreciation, and Amortization
}

df3 = pd.DataFrame(df3)
df4 = pd.DataFrame(df4)

df_long3 = df3.melt('Year', var_name='Category', value_name='Value')
df_long4 = df4.melt('Year', var_name='Category', value_name='Value')


# Define the function to create a line chart with points and value labels
def create_line_chart(df, year_col, value_col, category_col, value_title, plot_title):
    base_chart = alt.Chart(df).encode(
        x=alt.X(f"{year_col}:O", axis=alt.Axis(title=year_col, labelColor='black', titleColor='black')),
        y=alt.Y(f"{value_col}:Q", axis=alt.Axis(title=value_title, labelColor='black', titleColor='black')),
        color=alt.Color(f"{category_col}:N", legend=alt.Legend(title='Categories', orient='bottom')),
    ).properties(
        height=450,  # Setting the height of the plot
        title=plot_title  # Setting the title of the plot
    )
    
    # Define the line part of the chart
    line_chart = base_chart.mark_line(point=True).encode(
        size=alt.value(3)  # Line thickness
    )
    
    # Define the point part of the chart
    point_chart = base_chart.mark_point(filled=True, size=100).encode(
        tooltip=[f"{year_col}:O", f"{category_col}:N", f"{value_col}:Q"],
        color=alt.Color(f"{category_col}:N", scale=alt.Scale(domain=['Umsatz', 'EBITDA'], range=['#1f77b4', '#2ca02c']))
    )

    # Define the text part of the chart
    text_chart = base_chart.mark_text(
        align='center',
        dy=-10,  # Nudge text up so it doesn't overlap with the points
        fontWeight='bold'
    ).encode(
        text=alt.Text(f"{value_col}:Q", format=',')
    )

    # Layer the text marks on top of the bar chart
    final_chart = (point_chart + line_chart + text_chart)

    # Display the chart in Streamlit
    st.altair_chart(final_chart, use_container_width=True)

# Create the chart using the function
line_chart1 = create_line_chart(df_long3, 'Year', 'Value', 'Category', '€', 'Umsatz & EBITDA pro Zimmer')
line_chart2 = create_line_chart(df_long4, 'Year', 'Value', 'Category', '€', 'Umsatz & EBITDA pro Nächtigung')
