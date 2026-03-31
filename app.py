import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
import requests

# 1. Page Configuration
st.set_page_config(page_title="PhonePe Pulse Analysis", layout="wide")
st.title("🇮🇳 PhonePe Pulse Data Visualization (2018 - 2024)")
st.markdown("### Transaction and User Insights")

# 2. Database Connection Function
def get_data(query):
    conn = sqlite3.connect('phonepe_data.db')
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

# 3. Sidebar Filters
st.sidebar.header("Select Details")
year = st.sidebar.selectbox("Year", [2018, 2019, 2020, 2021, 2022, 2023, 2024])
quarter = st.sidebar.radio("Quarter", [1, 2, 3, 4])

# 4. Fetch Data based on Filters
query = f"""
    SELECT State, Transaction_Type, Transaction_Count, Transaction_Amount 
    FROM aggregated_transaction 
    WHERE Year = {year} AND Quarter = {quarter}
"""
df = get_data(query)

# 5. Creating Tabs for different Views
tab1, tab2 = st.tabs(["Geographical Analysis", "Transaction Trends"])

with tab1:
    st.subheader(f"State-wise Transaction Amount for Q{quarter}, {year}")
    
    # Aggregate data for the map
    map_df = df.groupby("State")["Transaction_Amount"].sum().reset_index()
    
    # India GeoJSON URL
    india_states_url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d117ad557e1f9a144fa/raw/e3833318e5172bda3527933190e0e88287c99fd1/india_states.geojson"
    
    # Plotly Map
    fig = px.choropleth(
        map_df,
        geojson=india_states_url,
        featureidkey="properties.ST_NM",
        locations="State",
        color="Transaction_Amount",
        color_continuous_scale="Reds",
        hover_name="State",
        title="Transaction Volume by State"
    )
    fig.update_geos(fitbounds="locations", visible=False)
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Transaction Categories")
        fig_pie = px.pie(df, values='Transaction_Amount', names='Transaction_Type', hole=0.4)
        st.plotly_chart(fig_pie)
        
    with col2:
        st.subheader("Top Performing States")
        top_states = map_df.sort_values(by="Transaction_Amount", ascending=False).head(10)
        fig_bar = px.bar(top_states, x="State", y="Transaction_Amount", color="Transaction_Amount")
        st.plotly_chart(fig_bar)

# 6. Key Insights Box
st.info(f"Summary: In Q{quarter} of {year}, the total transaction amount processed was ₹{df['Transaction_Amount'].sum():,.2f}")