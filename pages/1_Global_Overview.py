import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# =====================================
# PAGE CONFIG
# =====================================

st.set_page_config(
    page_title="Global Overview",
    page_icon="🌍",
    layout="wide"
)

# =====================================
# LOAD DATA
# =====================================

@st.cache_data
def load_data():
    return pd.read_csv(
        "data/global_nuclear_energy_intelligence_1965_2025.csv"
    )

df = load_data()

# =====================================
# TITLE
# =====================================

st.title("🌍 Global Nuclear Energy Overview")
st.markdown(
    "Comprehensive analysis of global nuclear energy production, carbon emissions, and decarbonisation trends."
)

st.markdown("---")

# =====================================
# SIDEBAR FILTERS
# =====================================

st.sidebar.header("Overview Filters")

year_min = int(df["year"].min())
year_max = int(df["year"].max())

selected_year = st.sidebar.slider(
    "Select Year",
    year_min,
    year_max,
    year_max
)

data_year = df[df["year"] == selected_year]

# =====================================
# KPI SECTION
# =====================================

st.subheader("📈 Global KPIs")

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric(
    "Countries",
    data_year["country"].nunique()
)

col2.metric(
    "Year",
    selected_year
)

col3.metric(
    "Total Nuclear Electricity",
    f"{data_year['nuclear_electricity'].sum():,.0f}"
)

col4.metric(
    "Avg CO₂ Per Capita",
    f"{data_year['co2_per_capita_t'].mean():.2f}"
)

col5.metric(
    "Avg Decarbonisation",
    f"{data_year['decarbonisation_score'].mean():.2f}"
)

st.markdown("---")

# =====================================
# GLOBAL NUCLEAR TREND
# =====================================

st.subheader("⚛ Global Nuclear Electricity Trend")

yearly_nuclear = (
    df.groupby("year")["nuclear_electricity"]
    .sum()
    .reset_index()
)

fig1 = px.line(
    yearly_nuclear,
    x="year",
    y="nuclear_electricity",
    markers=True,
    title="Global Nuclear Electricity Production"
)

fig1.update_layout(
    xaxis_title="Year",
    yaxis_title="Electricity Production"
)

st.plotly_chart(
    fig1,
    use_container_width=True
)

# =====================================
# LOW CARBON TREND
# =====================================

st.subheader("🌱 Low Carbon Electricity Growth")

energy_trend = (
    df.groupby("year")[
        [
            "nuclear_electricity",
            "renewables_electricity"
        ]
    ]
    .sum()
    .reset_index()
)

fig2 = px.line(
    energy_trend,
    x="year",
    y=[
        "nuclear_electricity",
        "renewables_electricity"
    ],
    title="Nuclear vs Renewable Electricity"
)

st.plotly_chart(
    fig2,
    use_container_width=True
)

# =====================================
# TOP NUCLEAR COUNTRIES
# =====================================

st.subheader("🏆 Top Nuclear Energy Producers")

top_nuclear = data_year.nlargest(
    10,
    "nuclear_electricity"
)

fig3 = px.bar(
    top_nuclear,
    x="country",
    y="nuclear_electricity",
    color="nuclear_electricity",
    text_auto=".2s",
    title=f"Top 10 Nuclear Producers ({selected_year})"
)

st.plotly_chart(
    fig3,
    use_container_width=True
)

# =====================================
# DECARBONISATION LEADERS
# =====================================

st.subheader("🌿 Decarbonisation Leaders")

leaders = data_year.nlargest(
    10,
    "decarbonisation_score"
)

fig4 = px.bar(
    leaders,
    x="country",
    y="decarbonisation_score",
    color="decarbonisation_score",
    text_auto=".2f",
    title=f"Top Decarbonisation Countries ({selected_year})"
)

st.plotly_chart(
    fig4,
    use_container_width=True
)

# =====================================
# NUCLEAR SHARE MAP
# =====================================

st.subheader("🗺 Nuclear Share by Country")

if "iso3" in data_year.columns:

    fig5 = px.choropleth(
        data_year,
        locations="iso3",
        color="nuclear_share_elec",
        hover_name="country",
        title=f"Nuclear Share of Electricity ({selected_year})",
        color_continuous_scale="Viridis"
    )

    st.plotly_chart(
        fig5,
        use_container_width=True
    )

# =====================================
# CARBON ANALYSIS
# =====================================

st.subheader("🌍 Carbon Emissions Analysis")

fig6 = px.scatter(
    data_year,
    x="nuclear_share_elec",
    y="co2_per_capita_t",
    size="population",
    hover_name="country",
    color="decarbonisation_score",
    title="Nuclear Share vs CO₂ Emissions"
)

st.plotly_chart(
    fig6,
    use_container_width=True
)

# =====================================
# GLOBAL ENERGY MIX
# =====================================

st.subheader("⚡ Energy Mix")

energy_mix = {
    "Nuclear":
        data_year["nuclear_electricity"].sum(),

    "Renewables":
        data_year["renewables_electricity"].sum()
}

energy_df = pd.DataFrame(
    {
        "Source": energy_mix.keys(),
        "Value": energy_mix.values()
    }
)

fig7 = px.pie(
    energy_df,
    names="Source",
    values="Value",
    hole=0.4,
    title="Global Low Carbon Electricity Mix"
)

st.plotly_chart(
    fig7,
    use_container_width=True
)

# =====================================
# YEARLY DECARBONISATION TREND
# =====================================

st.subheader("📉 Global Decarbonisation Trend")

decarbon = (
    df.groupby("year")[
        "decarbonisation_score"
    ]
    .mean()
    .reset_index()
)

fig8 = px.area(
    decarbon,
    x="year",
    y="decarbonisation_score",
    title="Average Global Decarbonisation Score"
)

st.plotly_chart(
    fig8,
    use_container_width=True
)

# =====================================
# EXECUTIVE INSIGHTS
# =====================================

st.subheader("🤖 Executive Insights")

highest_nuclear_country = top_nuclear.iloc[0]["country"]

highest_decarbon_country = leaders.iloc[0]["country"]

avg_co2 = round(
    data_year["co2_per_capita_t"].mean(),
    2
)

st.success(
    f"🏆 Highest Nuclear Producer in {selected_year}: {highest_nuclear_country}"
)

st.info(
    f"🌿 Best Decarbonisation Score in {selected_year}: {highest_decarbon_country}"
)

st.warning(
    f"🌍 Average CO₂ per Capita: {avg_co2} tons"
)

st.markdown(
"""
### Key Findings

- Nuclear power remains a major contributor to low-carbon electricity generation.
- Countries with higher nuclear share generally show lower carbon intensity.
- Renewable energy has accelerated rapidly in the last two decades.
- Decarbonisation performance is strongest in countries combining nuclear and renewables.
- Global low-carbon electricity production continues to grow steadily.
"""
)

# =====================================
# DATA TABLE
# =====================================

st.subheader("📋 Selected Year Data")

st.dataframe(
    data_year,
    use_container_width=True
)

# =====================================
# DOWNLOAD
# =====================================

csv = data_year.to_csv(index=False)

st.download_button(
    label="⬇ Download Current Data",
    data=csv,
    file_name=f"global_overview_{selected_year}.csv",
    mime="text/csv"
)

st.markdown("---")
st.caption(
    "Global Nuclear Energy Intelligence Dashboard | Streamlit + Plotly"
)
