import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import seaborn as sns
import matplotlib.pyplot as plt

from sklearn.ensemble import RandomForestRegressor

# -----------------------------------
# PAGE CONFIG
# -----------------------------------

st.set_page_config(
    page_title="Global Nuclear Energy Intelligence Dashboard",
    page_icon="⚛️",
    layout="wide"
)

# -----------------------------------
# LOAD DATA
# -----------------------------------

@st.cache_data
def load_data():
    df = pd.read_csv(
        "data/global_nuclear_energy_intelligence_1965_2025.csv"
    )
    return df

df = load_data()

# -----------------------------------
# TITLE
# -----------------------------------

st.title("⚛️ Global Nuclear Energy Intelligence Dashboard")
st.markdown("---")

# -----------------------------------
# SIDEBAR
# -----------------------------------

st.sidebar.header("Filters")

countries = sorted(df["country"].unique())

selected_country = st.sidebar.multiselect(
    "Select Country",
    countries,
    default=countries[:5]
)

year_range = st.sidebar.slider(
    "Select Year Range",
    int(df["year"].min()),
    int(df["year"].max()),
    (
        int(df["year"].min()),
        int(df["year"].max())
    )
)

filtered_df = df[
    (df["country"].isin(selected_country))
    &
    (df["year"] >= year_range[0])
    &
    (df["year"] <= year_range[1])
]

# -----------------------------------
# KPI SECTION
# -----------------------------------

st.subheader("📈 Key Performance Indicators")

col1,col2,col3,col4 = st.columns(4)

col1.metric(
    "Countries",
    df["country"].nunique()
)

col2.metric(
    "Latest Year",
    int(df["year"].max())
)

col3.metric(
    "Total Nuclear Electricity",
    f"{df['nuclear_electricity'].sum():,.0f}"
)

col4.metric(
    "Avg Decarbonisation",
    round(df["decarbonisation_score"].mean(),2)
)

st.markdown("---")

# -----------------------------------
# GLOBAL NUCLEAR TREND
# -----------------------------------

st.subheader("🌍 Global Nuclear Electricity Trend")

global_trend = (
    df.groupby("year")["nuclear_electricity"]
    .sum()
    .reset_index()
)

fig = px.line(
    global_trend,
    x="year",
    y="nuclear_electricity",
    markers=True,
    title="Global Nuclear Electricity Production"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# -----------------------------------
# NUCLEAR VS RENEWABLES
# -----------------------------------

st.subheader("⚡ Nuclear vs Renewable Electricity")

energy = (
    df.groupby("year")
    [
        [
            "nuclear_electricity",
            "renewables_electricity"
        ]
    ]
    .sum()
    .reset_index()
)

fig2 = px.line(
    energy,
    x="year",
    y=[
        "nuclear_electricity",
        "renewables_electricity"
    ],
    title="Nuclear vs Renewable Growth"
)

st.plotly_chart(
    fig2,
    use_container_width=True
)

# -----------------------------------
# COUNTRY ANALYSIS
# -----------------------------------

st.subheader("🏆 Country Comparison")

fig3 = px.line(
    filtered_df,
    x="year",
    y="nuclear_electricity",
    color="country",
    title="Country Nuclear Electricity Trend"
)

st.plotly_chart(
    fig3,
    use_container_width=True
)

# -----------------------------------
# TOP 10 COUNTRIES
# -----------------------------------

st.subheader("🌎 Top Nuclear Energy Producers")

latest_year = df["year"].max()

latest = df[
    df["year"] == latest_year
]

top10 = latest.nlargest(
    10,
    "nuclear_electricity"
)

fig4 = px.bar(
    top10,
    x="country",
    y="nuclear_electricity",
    color="nuclear_electricity",
    title="Top 10 Nuclear Producers"
)

st.plotly_chart(
    fig4,
    use_container_width=True
)

# -----------------------------------
# CARBON ANALYSIS
# -----------------------------------

st.subheader("🌱 Carbon Emission Analysis")

fig5 = px.scatter(
    latest,
    x="nuclear_share_elec",
    y="co2_per_capita_t",
    color="country",
    size="population",
    hover_name="country",
    title="Nuclear Share vs CO₂ Emissions"
)

st.plotly_chart(
    fig5,
    use_container_width=True
)

# -----------------------------------
# CORRELATION HEATMAP
# -----------------------------------

st.subheader("🔥 Correlation Heatmap")

corr_features = [
    "nuclear_electricity",
    "renewables_electricity",
    "co2_per_capita_t",
    "decarbonisation_score",
    "gdp_per_capita_usd"
]

corr = df[corr_features].corr()

fig6, ax = plt.subplots(
    figsize=(10,6)
)

sns.heatmap(
    corr,
    annot=True,
    cmap="coolwarm",
    ax=ax
)

st.pyplot(fig6)

# -----------------------------------
# DECARBONISATION LEADERS
# -----------------------------------

st.subheader("🏅 Decarbonisation Leaders")

leaders = latest.nlargest(
    15,
    "decarbonisation_score"
)

fig7 = px.bar(
    leaders,
    x="country",
    y="decarbonisation_score",
    color="decarbonisation_score",
    title="Top Decarbonisation Countries"
)

st.plotly_chart(
    fig7,
    use_container_width=True
)

# -----------------------------------
# FORECASTING
# -----------------------------------

st.subheader("🔮 Nuclear Electricity Forecast")

forecast_country = st.selectbox(
    "Select Country for Forecast",
    countries
)

country_df = df[
    df["country"] == forecast_country
]

country_df = country_df.sort_values(
    "year"
)

X = country_df[["year"]]
y = country_df["nuclear_electricity"]

model = RandomForestRegressor(
    n_estimators=200,
    random_state=42
)

model.fit(X,y)

future_years = pd.DataFrame({
    "year":[
        2026,
        2027,
        2028,
        2029,
        2030
    ]
})

predictions = model.predict(
    future_years
)

future_years["Forecast"] = predictions

fig8 = go.Figure()

fig8.add_trace(
    go.Scatter(
        x=country_df["year"],
        y=country_df["nuclear_electricity"],
        mode="lines",
        name="Historical"
    )
)

fig8.add_trace(
    go.Scatter(
        x=future_years["year"],
        y=future_years["Forecast"],
        mode="lines+markers",
        name="Forecast"
    )
)

fig8.update_layout(
    title=f"{forecast_country} Forecast"
)

st.plotly_chart(
    fig8,
    use_container_width=True
)

st.dataframe(future_years)

# -----------------------------------
# AI INSIGHTS
# -----------------------------------

st.subheader("🤖 AI Generated Insights")

highest_country = latest.loc[
    latest["nuclear_electricity"].idxmax(),
    "country"
]

lowest_emission = latest.loc[
    latest["co2_per_capita_t"].idxmin(),
    "country"
]

st.success(
    f"🏆 Highest Nuclear Producer: {highest_country}"
)

st.info(
    f"🌱 Lowest CO₂ Per Capita: {lowest_emission}"
)

st.warning(
    f"⚡ Average Decarbonisation Score: {round(df['decarbonisation_score'].mean(),2)}"
)

# -----------------------------------
# DATA DOWNLOAD
# -----------------------------------

st.subheader("⬇ Download Dataset")

csv = df.to_csv(index=False)

st.download_button(
    label="Download CSV",
    data=csv,
    file_name="nuclear_energy_data.csv",
    mime="text/csv"
)

# -----------------------------------
# RAW DATA
# -----------------------------------

with st.expander("View Raw Data"):
    st.dataframe(df)

st.markdown("---")
st.caption(
    "Developed using Streamlit | Plotly | Machine Learning | Data Analytics"
)
