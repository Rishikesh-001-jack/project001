import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# ==================================================
# PAGE CONFIG
# ==================================================

st.set_page_config(
    page_title="Nuclear vs Renewables",
    page_icon="⚡",
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

st.title("⚡ Nuclear Energy vs Renewable Energy")

st.markdown("""
Compare global and country-level performance of:

- Nuclear Electricity
- Renewable Electricity
- Energy Mix
- Growth Trends
- Decarbonisation Impact
""")

st.markdown("---")

# ==================================================
# SIDEBAR
# ==================================================

st.sidebar.header("Comparison Filters")

countries = sorted(df["country"].unique())

selected_countries = st.sidebar.multiselect(
    "Select Countries",
    countries,
    default=countries[:5]
)

selected_year = st.sidebar.slider(
    "Year",
    int(df["year"].min()),
    int(df["year"].max()),
    int(df["year"].max())
)

filtered_df = df[
    df["country"].isin(selected_countries)
]

latest = df[
    df["year"] == selected_year
]

# ==================================================
# KPI SECTION
# ==================================================

st.subheader("📊 Global Energy KPIs")

latest_global = latest.copy()

total_nuclear = latest_global[
    "nuclear_electricity"
].sum()

total_renewables = latest_global[
    "renewables_electricity"
].sum()

nuclear_share = (
    total_nuclear /
    (total_nuclear + total_renewables)
) * 100

renewable_share = (
    total_renewables /
    (total_nuclear + total_renewables)
) * 100

col1,col2,col3,col4 = st.columns(4)

col1.metric(
    "Nuclear Electricity",
    f"{total_nuclear:,.0f}"
)

col2.metric(
    "Renewables Electricity",
    f"{total_renewables:,.0f}"
)

col3.metric(
    "Nuclear Share",
    f"{nuclear_share:.1f}%"
)

col4.metric(
    "Renewable Share",
    f"{renewable_share:.1f}%"
)

st.markdown("---")

# ==================================================
# GLOBAL TREND
# ==================================================

st.subheader("🌍 Global Trend")

global_energy = (
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

fig1 = px.line(
    global_energy,
    x="year",
    y=[
        "nuclear_electricity",
        "renewables_electricity"
    ],
    title="Global Nuclear vs Renewables"
)

st.plotly_chart(
    fig1,
    use_container_width=True
)

# ==================================================
# ENERGY MIX
# ==================================================

st.subheader("⚡ Global Energy Mix")

energy_mix = pd.DataFrame({
    "Source": [
        "Nuclear",
        "Renewables"
    ],
    "Electricity": [
        total_nuclear,
        total_renewables
    ]
})

fig2 = px.pie(
    energy_mix,
    names="Source",
    values="Electricity",
    hole=0.5,
    title=f"Energy Mix ({selected_year})"
)

st.plotly_chart(
    fig2,
    use_container_width=True
)

# ==================================================
# COUNTRY COMPARISON
# ==================================================

st.subheader("🌎 Country Comparison")

country_compare = filtered_df[
    [
        "country",
        "year",
        "nuclear_electricity",
        "renewables_electricity"
    ]
]

fig3 = px.line(
    country_compare,
    x="year",
    y=[
        "nuclear_electricity",
        "renewables_electricity"
    ],
    color="country",
    title="Country-Level Comparison"
)

st.plotly_chart(
    fig3,
    use_container_width=True
)

# ==================================================
# TOP NUCLEAR COUNTRIES
# ==================================================

st.subheader("🏆 Top Nuclear Producers")

top_nuclear = latest.nlargest(
    10,
    "nuclear_electricity"
)

fig4 = px.bar(
    top_nuclear,
    x="country",
    y="nuclear_electricity",
    color="nuclear_electricity",
    text_auto=".2s",
    title=f"Top Nuclear Countries ({selected_year})"
)

st.plotly_chart(
    fig4,
    use_container_width=True
)

# ==================================================
# TOP RENEWABLE COUNTRIES
# ==================================================

st.subheader("🌱 Top Renewable Producers")

top_renewable = latest.nlargest(
    10,
    "renewables_electricity"
)

fig5 = px.bar(
    top_renewable,
    x="country",
    y="renewables_electricity",
    color="renewables_electricity",
    text_auto=".2s",
    title=f"Top Renewable Countries ({selected_year})"
)

st.plotly_chart(
    fig5,
    use_container_width=True
)

# ==================================================
# NUCLEAR SHARE RANKING
# ==================================================

st.subheader("⚛ Top Nuclear Share Countries")

top_share = latest.nlargest(
    15,
    "nuclear_share_elec"
)

fig6 = px.bar(
    top_share,
    x="country",
    y="nuclear_share_elec",
    color="nuclear_share_elec",
    title="Highest Nuclear Share"
)

st.plotly_chart(
    fig6,
    use_container_width=True
)

# ==================================================
# RENEWABLE SHARE RANKING
# ==================================================

renewable_share_col = None

for col in latest.columns:
    if "renewable_share" in col.lower():
        renewable_share_col = col
        break

if renewable_share_col:

    st.subheader("🌿 Renewable Share Leaders")

    top_renew = latest.nlargest(
        15,
        renewable_share_col
    )

    fig7 = px.bar(
        top_renew,
        x="country",
        y=renewable_share_col,
        color=renewable_share_col
    )

    st.plotly_chart(
        fig7,
        use_container_width=True
    )

# ==================================================
# GROWTH RATE ANALYSIS
# ==================================================

st.subheader("📈 Growth Rate Analysis")

growth = global_energy.copy()

growth["nuclear_growth"] = (
    growth["nuclear_electricity"]
    .pct_change() * 100
)

growth["renewable_growth"] = (
    growth["renewables_electricity"]
    .pct_change() * 100
)

fig8 = px.line(
    growth,
    x="year",
    y=[
        "nuclear_growth",
        "renewable_growth"
    ],
    title="Growth Rate (%)"
)

st.plotly_chart(
    fig8,
    use_container_width=True
)

# ==================================================
# CORRELATION ANALYSIS
# ==================================================

st.subheader("🔥 Correlation Analysis")

corr_cols = [
    "nuclear_electricity",
    "renewables_electricity",
    "co2_per_capita_t",
    "decarbonisation_score",
    "gdp_per_capita_usd"
]

corr = df[corr_cols].corr()

fig9, ax = plt.subplots(
    figsize=(8,5)
)

sns.heatmap(
    corr,
    annot=True,
    cmap="coolwarm",
    ax=ax
)

st.pyplot(fig9)

# ==================================================
# NUCLEAR VS CO2
# ==================================================

st.subheader("🌍 Nuclear Share vs CO₂")

fig10 = px.scatter(
    latest,
    x="nuclear_share_elec",
    y="co2_per_capita_t",
    size="population",
    color="decarbonisation_score",
    hover_name="country",
    title="Nuclear Share and Emissions"
)

st.plotly_chart(
    fig10,
    use_container_width=True
)

# ==================================================
# INSIGHTS
# ==================================================

st.subheader("🤖 Executive Insights")

best_nuclear = latest.loc[
    latest["nuclear_electricity"].idxmax()
]["country"]

best_renewable = latest.loc[
    latest["renewables_electricity"].idxmax()
]["country"]

st.success(
    f"⚛ Largest Nuclear Producer: {best_nuclear}"
)

st.info(
    f"🌱 Largest Renewable Producer: {best_renewable}"
)

st.warning(
    f"⚡ Nuclear contributes approximately "
    f"{nuclear_share:.1f}% of total low-carbon electricity."
)

st.markdown("""
### Key Findings

- Renewable energy is growing faster globally.
- Nuclear energy remains one of the largest sources of low-carbon electricity.
- Countries combining nuclear and renewables generally achieve better decarbonisation scores.
- Higher nuclear share often corresponds with lower carbon intensity.
- Energy diversification improves energy security and sustainability.
""")

# ==================================================
# DATA TABLE
# ==================================================

st.subheader("📋 Comparison Dataset")

st.dataframe(
    latest,
    use_container_width=True
)

# ==================================================
# DOWNLOAD
# ==================================================

csv = latest.to_csv(index=False)

st.download_button(
    "⬇ Download Comparison Data",
    csv,
    file_name="nuclear_vs_renewables.csv",
    mime="text/csv"
)

st.markdown("---")

st.caption(
    "Nuclear vs Renewables Analytics | Streamlit Dashboard"
)
