import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import seaborn as sns
import matplotlib.pyplot as plt

from sklearn.ensemble import RandomForestRegressor

# ==================================================
# PAGE CONFIG
# ==================================================

st.set_page_config(
    page_title="Country Analytics",
    page_icon="🌎",
    layout="wide"
)

# ==================================================
# LOAD DATA
# ==================================================

@st.cache_data
def load_data():
    return pd.read_csv(
        "data/global_nuclear_energy_intelligence_1965_2025.csv"
    )

df = load_data()

# ==================================================
# TITLE
# ==================================================

st.title("🌎 Country Analytics Dashboard")

st.markdown("""
Analyze nuclear energy performance, carbon emissions,
economic growth, and decarbonisation progress for
individual countries.
""")

st.markdown("---")

# ==================================================
# SIDEBAR
# ==================================================

st.sidebar.header("Country Filters")

countries = sorted(
    df["country"].unique()
)

selected_country = st.sidebar.selectbox(
    "Select Country",
    countries
)

country_df = df[
    df["country"] == selected_country
].copy()

country_df = country_df.sort_values(
    "year"
)

# ==================================================
# KPI SECTION
# ==================================================

latest = country_df.iloc[-1]

st.subheader("📈 Country KPIs")

col1,col2,col3,col4,col5 = st.columns(5)

col1.metric(
    "Latest Year",
    int(latest["year"])
)

col2.metric(
    "Nuclear Electricity",
    f"{latest['nuclear_electricity']:,.2f}"
)

col3.metric(
    "Renewables",
    f"{latest['renewables_electricity']:,.2f}"
)

col4.metric(
    "CO₂ Per Capita",
    f"{latest['co2_per_capita_t']:.2f}"
)

col5.metric(
    "Decarbonisation",
    f"{latest['decarbonisation_score']:.2f}"
)

st.markdown("---")

# ==================================================
# NUCLEAR ELECTRICITY TREND
# ==================================================

st.subheader("⚛ Nuclear Electricity Trend")

fig1 = px.line(
    country_df,
    x="year",
    y="nuclear_electricity",
    markers=True,
    title=f"{selected_country} Nuclear Electricity Production"
)

st.plotly_chart(
    fig1,
    use_container_width=True
)

# ==================================================
# RENEWABLE ELECTRICITY TREND
# ==================================================

st.subheader("🌱 Renewable Electricity Trend")

fig2 = px.line(
    country_df,
    x="year",
    y="renewables_electricity",
    markers=True,
    title=f"{selected_country} Renewable Electricity"
)

st.plotly_chart(
    fig2,
    use_container_width=True
)

# ==================================================
# NUCLEAR VS RENEWABLES
# ==================================================

st.subheader("⚡ Nuclear vs Renewable Comparison")

energy_compare = country_df[
    [
        "year",
        "nuclear_electricity",
        "renewables_electricity"
    ]
]

fig3 = px.line(
    energy_compare,
    x="year",
    y=[
        "nuclear_electricity",
        "renewables_electricity"
    ],
    title=f"{selected_country}: Nuclear vs Renewables"
)

st.plotly_chart(
    fig3,
    use_container_width=True
)

# ==================================================
# CARBON TREND
# ==================================================

st.subheader("🌍 CO₂ Emission Trend")

fig4 = px.area(
    country_df,
    x="year",
    y="co2_per_capita_t",
    title=f"{selected_country} CO₂ Per Capita"
)

st.plotly_chart(
    fig4,
    use_container_width=True
)

# ==================================================
# DECARBONISATION TREND
# ==================================================

st.subheader("🌿 Decarbonisation Trend")

fig5 = px.line(
    country_df,
    x="year",
    y="decarbonisation_score",
    markers=True,
    title=f"{selected_country} Decarbonisation Score"
)

st.plotly_chart(
    fig5,
    use_container_width=True
)

# ==================================================
# NUCLEAR SHARE TREND
# ==================================================

st.subheader("⚡ Nuclear Share of Electricity")

fig6 = px.bar(
    country_df,
    x="year",
    y="nuclear_share_elec",
    title=f"{selected_country} Nuclear Share (%)"
)

st.plotly_chart(
    fig6,
    use_container_width=True
)

# ==================================================
# GDP VS NUCLEAR
# ==================================================

st.subheader("💰 GDP vs Nuclear Electricity")

fig7 = px.scatter(
    country_df,
    x="gdp_per_capita_usd",
    y="nuclear_electricity",
    size="population",
    hover_name="country",
    color="decarbonisation_score",
    title="GDP Per Capita vs Nuclear Production"
)

st.plotly_chart(
    fig7,
    use_container_width=True
)

# ==================================================
# CORRELATION ANALYSIS
# ==================================================

st.subheader("🔥 Correlation Analysis")

corr_columns = [
    "nuclear_electricity",
    "renewables_electricity",
    "co2_per_capita_t",
    "decarbonisation_score",
    "gdp_per_capita_usd"
]

corr = country_df[corr_columns].corr()

fig8, ax = plt.subplots(
    figsize=(8,5)
)

sns.heatmap(
    corr,
    annot=True,
    cmap="coolwarm",
    ax=ax
)

st.pyplot(fig8)

# ==================================================
# FORECASTING
# ==================================================

st.subheader("🔮 Nuclear Electricity Forecast")

X = country_df[["year"]]
y = country_df["nuclear_electricity"]

model = RandomForestRegressor(
    n_estimators=200,
    random_state=42
)

model.fit(X,y)

future_years = pd.DataFrame({
    "year":[2026,2027,2028,2029,2030]
})

future_years["forecast"] = model.predict(
    future_years
)

fig9 = go.Figure()

fig9.add_trace(
    go.Scatter(
        x=country_df["year"],
        y=country_df["nuclear_electricity"],
        mode="lines",
        name="Historical"
    )
)

fig9.add_trace(
    go.Scatter(
        x=future_years["year"],
        y=future_years["forecast"],
        mode="lines+markers",
        name="Forecast"
    )
)

fig9.update_layout(
    title=f"{selected_country} Nuclear Forecast (2030)"
)

st.plotly_chart(
    fig9,
    use_container_width=True
)

st.dataframe(
    future_years,
    use_container_width=True
)

# ==================================================
# AI INSIGHTS
# ==================================================

st.subheader("🤖 AI Insights")

max_nuclear = country_df.loc[
    country_df["nuclear_electricity"].idxmax()
]

min_co2 = country_df.loc[
    country_df["co2_per_capita_t"].idxmin()
]

max_decarbon = country_df.loc[
    country_df["decarbonisation_score"].idxmax()
]

st.success(
    f"🏆 Highest Nuclear Production: {max_nuclear['year']} "
    f"({max_nuclear['nuclear_electricity']:,.2f})"
)

st.info(
    f"🌍 Lowest CO₂ Emissions: {min_co2['year']} "
    f"({min_co2['co2_per_capita_t']:.2f})"
)

st.warning(
    f"🌿 Best Decarbonisation Score: {max_decarbon['year']} "
    f"({max_decarbon['decarbonisation_score']:.2f})"
)

# ==================================================
# SUMMARY TABLE
# ==================================================

st.subheader("📋 Country Dataset")

st.dataframe(
    country_df,
    use_container_width=True
)

# ==================================================
# DOWNLOAD
# ==================================================

csv = country_df.to_csv(index=False)

st.download_button(
    "⬇ Download Country Data",
    csv,
    file_name=f"{selected_country}_analytics.csv",
    mime="text/csv"
)

st.markdown("---")

st.caption(
    "Country Analytics | Nuclear Energy Intelligence Dashboard"
)
