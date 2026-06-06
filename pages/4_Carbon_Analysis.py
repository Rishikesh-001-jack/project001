import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import seaborn as sns
import matplotlib.pyplot as plt

from sklearn.ensemble import RandomForestRegressor

# ======================================================
# PAGE CONFIG
# ======================================================

st.set_page_config(
    page_title="Carbon Analysis",
    page_icon="🌍",
    layout="wide"
)

# ======================================================
# LOAD DATA
# ======================================================

@st.cache_data
def load_data():
    return pd.read_csv(
        "data/global_nuclear_energy_intelligence_1965_2025.csv"
    )

df = load_data()

# ======================================================
# TITLE
# ======================================================

st.title("🌍 Carbon Emissions Analysis Dashboard")

st.markdown("""
Analyze:

- Carbon Emissions
- Nuclear Impact
- Renewable Impact
- Decarbonisation Progress
- Carbon Intensity
- Future Emission Trends
""")

st.markdown("---")

# ======================================================
# SIDEBAR
# ======================================================

st.sidebar.header("Carbon Filters")

countries = sorted(df["country"].unique())

selected_country = st.sidebar.selectbox(
    "Select Country",
    countries
)

selected_year = st.sidebar.slider(
    "Select Year",
    int(df["year"].min()),
    int(df["year"].max()),
    int(df["year"].max())
)

country_df = df[
    df["country"] == selected_country
].sort_values("year")

latest = df[
    df["year"] == selected_year
]

# ======================================================
# KPI SECTION
# ======================================================

st.subheader("📊 Carbon KPIs")

latest_country = country_df.iloc[-1]

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "CO₂ Per Capita",
    f"{latest_country['co2_per_capita_t']:.2f}"
)

col2.metric(
    "Nuclear Share",
    f"{latest_country['nuclear_share_elec']:.2f}%"
)

col3.metric(
    "Decarbonisation Score",
    f"{latest_country['decarbonisation_score']:.2f}"
)

col4.metric(
    "Year",
    int(latest_country["year"])
)

st.markdown("---")

# ======================================================
# GLOBAL CO2 TREND
# ======================================================

st.subheader("🌎 Global CO₂ Trend")

global_co2 = (
    df.groupby("year")["co2_per_capita_t"]
    .mean()
    .reset_index()
)

fig1 = px.line(
    global_co2,
    x="year",
    y="co2_per_capita_t",
    markers=True,
    title="Average Global CO₂ Per Capita"
)

st.plotly_chart(
    fig1,
    use_container_width=True
)

# ======================================================
# COUNTRY CO2 TREND
# ======================================================

st.subheader(f"📈 {selected_country} CO₂ Trend")

fig2 = px.area(
    country_df,
    x="year",
    y="co2_per_capita_t",
    title=f"{selected_country} CO₂ Emissions"
)

st.plotly_chart(
    fig2,
    use_container_width=True
)

# ======================================================
# NUCLEAR SHARE VS CO2
# ======================================================

st.subheader("⚛ Nuclear Share vs CO₂")

fig3 = px.scatter(
    latest,
    x="nuclear_share_elec",
    y="co2_per_capita_t",
    size="population",
    color="decarbonisation_score",
    hover_name="country",
    title="Nuclear Share vs CO₂ Emissions"
)

st.plotly_chart(
    fig3,
    use_container_width=True
)

# ======================================================
# RENEWABLES VS CO2
# ======================================================

st.subheader("🌱 Renewables vs CO₂")

fig4 = px.scatter(
    latest,
    x="renewables_electricity",
    y="co2_per_capita_t",
    size="population",
    hover_name="country",
    color="decarbonisation_score",
    title="Renewables vs CO₂ Emissions"
)

st.plotly_chart(
    fig4,
    use_container_width=True
)

# ======================================================
# CARBON INTENSITY RANKING
# ======================================================

st.subheader("🏭 Highest Carbon Intensity Countries")

highest_carbon = latest.nlargest(
    15,
    "co2_per_capita_t"
)

fig5 = px.bar(
    highest_carbon,
    x="country",
    y="co2_per_capita_t",
    color="co2_per_capita_t",
    title="Highest CO₂ Per Capita"
)

st.plotly_chart(
    fig5,
    use_container_width=True
)

# ======================================================
# LOWEST CARBON COUNTRIES
# ======================================================

st.subheader("🌿 Lowest Carbon Countries")

lowest_carbon = latest.nsmallest(
    15,
    "co2_per_capita_t"
)

fig6 = px.bar(
    lowest_carbon,
    x="country",
    y="co2_per_capita_t",
    color="co2_per_capita_t",
    title="Lowest CO₂ Per Capita"
)

st.plotly_chart(
    fig6,
    use_container_width=True
)

# ======================================================
# DECARBONISATION LEADERS
# ======================================================

st.subheader("🏆 Decarbonisation Leaders")

leaders = latest.nlargest(
    15,
    "decarbonisation_score"
)

fig7 = px.bar(
    leaders,
    x="country",
    y="decarbonisation_score",
    color="decarbonisation_score",
    title="Top Decarbonisation Scores"
)

st.plotly_chart(
    fig7,
    use_container_width=True
)

# ======================================================
# CO2 DISTRIBUTION
# ======================================================

st.subheader("📊 CO₂ Distribution")

fig8 = px.histogram(
    latest,
    x="co2_per_capita_t",
    nbins=30,
    title="Distribution of CO₂ Emissions"
)

st.plotly_chart(
    fig8,
    use_container_width=True
)

# ======================================================
# CORRELATION HEATMAP
# ======================================================

st.subheader("🔥 Correlation Analysis")

corr_cols = [
    "co2_per_capita_t",
    "nuclear_electricity",
    "renewables_electricity",
    "decarbonisation_score",
    "gdp_per_capita_usd"
]

corr = df[corr_cols].corr()

fig9, ax = plt.subplots(
    figsize=(10,6)
)

sns.heatmap(
    corr,
    annot=True,
    cmap="coolwarm",
    ax=ax
)

st.pyplot(fig9)

# ======================================================
# FORECASTING
# ======================================================

st.subheader("🔮 CO₂ Forecast (2030)")

X = country_df[["year"]]
y = country_df["co2_per_capita_t"]

model = RandomForestRegressor(
    n_estimators=200,
    random_state=42
)

model.fit(X, y)

future_years = pd.DataFrame({
    "year": [2026, 2027, 2028, 2029, 2030]
})

future_years["forecast_co2"] = model.predict(
    future_years
)

fig10 = go.Figure()

fig10.add_trace(
    go.Scatter(
        x=country_df["year"],
        y=country_df["co2_per_capita_t"],
        mode="lines",
        name="Historical"
    )
)

fig10.add_trace(
    go.Scatter(
        x=future_years["year"],
        y=future_years["forecast_co2"],
        mode="lines+markers",
        name="Forecast"
    )
)

fig10.update_layout(
    title=f"{selected_country} CO₂ Forecast"
)

st.plotly_chart(
    fig10,
    use_container_width=True
)

st.dataframe(
    future_years,
    use_container_width=True
)

# ======================================================
# EXECUTIVE INSIGHTS
# ======================================================

st.subheader("🤖 Executive Insights")

lowest_country = latest.loc[
    latest["co2_per_capita_t"].idxmin()
]["country"]

highest_country = latest.loc[
    latest["co2_per_capita_t"].idxmax()
]["country"]

best_decarbon = latest.loc[
    latest["decarbonisation_score"].idxmax()
]["country"]

st.success(
    f"🌿 Lowest CO₂ Country: {lowest_country}"
)

st.error(
    f"🏭 Highest CO₂ Country: {highest_country}"
)

st.info(
    f"🏆 Best Decarbonisation Score: {best_decarbon}"
)

st.markdown("""
### Key Findings

- Countries with higher nuclear participation often show lower carbon intensity.
- Renewable energy growth contributes significantly to emission reduction.
- Decarbonisation scores are strongly associated with low-carbon electricity adoption.
- Nations combining nuclear and renewables achieve better sustainability outcomes.
- Long-term emission trends indicate a gradual shift toward cleaner energy systems.
""")

# ======================================================
# DATA TABLE
# ======================================================

st.subheader("📋 Carbon Dataset")

st.dataframe(
    latest,
    use_container_width=True
)

# ======================================================
# DOWNLOAD
# ======================================================

csv = latest.to_csv(index=False)

st.download_button(
    label="⬇ Download Carbon Analysis Data",
    data=csv,
    file_name="carbon_analysis.csv",
    mime="text/csv"
)

st.markdown("---")

st.caption(
    "Carbon Analysis Dashboard | Streamlit + Plotly + Machine Learning"
)
