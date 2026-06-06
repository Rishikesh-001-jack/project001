import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# ======================================================
# PAGE CONFIG
# ======================================================

st.set_page_config(
    page_title="AI Insights",
    page_icon="🤖",
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

st.title("🤖 AI Insights & Executive Intelligence")

st.markdown("""
Automatically generated insights from:

- Nuclear Energy
- Renewable Energy
- Carbon Emissions
- Decarbonisation Progress
- Sustainability Indicators
""")

st.markdown("---")

# ======================================================
# SIDEBAR
# ======================================================

st.sidebar.header("AI Controls")

selected_year = st.sidebar.slider(
    "Analysis Year",
    int(df["year"].min()),
    int(df["year"].max()),
    int(df["year"].max())
)

latest = df[
    df["year"] == selected_year
].copy()

# ======================================================
# KPI SECTION
# ======================================================

st.subheader("📊 AI Executive KPIs")

col1,col2,col3,col4,col5 = st.columns(5)

col1.metric(
    "Countries",
    latest["country"].nunique()
)

col2.metric(
    "Nuclear Production",
    f"{latest['nuclear_electricity'].sum():,.0f}"
)

col3.metric(
    "Renewables",
    f"{latest['renewables_electricity'].sum():,.0f}"
)

col4.metric(
    "Avg CO₂",
    f"{latest['co2_per_capita_t'].mean():.2f}"
)

col5.metric(
    "Avg Decarbonisation",
    f"{latest['decarbonisation_score'].mean():.2f}"
)

st.markdown("---")

# ======================================================
# LEADERS
# ======================================================

highest_nuclear = latest.loc[
    latest["nuclear_electricity"].idxmax()
]

highest_renewable = latest.loc[
    latest["renewables_electricity"].idxmax()
]

lowest_carbon = latest.loc[
    latest["co2_per_capita_t"].idxmin()
]

highest_decarbon = latest.loc[
    latest["decarbonisation_score"].idxmax()
]

# ======================================================
# AI INSIGHTS CARDS
# ======================================================

st.subheader("🧠 AI Generated Insights")

c1,c2 = st.columns(2)

with c1:

    st.success(
        f"""
🏆 Highest Nuclear Producer

Country: {highest_nuclear['country']}

Production: {highest_nuclear['nuclear_electricity']:,.2f}
"""
    )

    st.info(
        f"""
🌿 Highest Renewable Producer

Country: {highest_renewable['country']}

Production: {highest_renewable['renewables_electricity']:,.2f}
"""
    )

with c2:

    st.success(
        f"""
🌍 Lowest Carbon Country

Country: {lowest_carbon['country']}

CO₂: {lowest_carbon['co2_per_capita_t']:.2f}
"""
    )

    st.info(
        f"""
⚡ Best Decarbonisation Country

Country: {highest_decarbon['country']}

Score: {highest_decarbon['decarbonisation_score']:.2f}
"""
    )

st.markdown("---")

# ======================================================
# TOP NUCLEAR COUNTRIES
# ======================================================

st.subheader("⚛ Nuclear Leadership")

top_nuclear = latest.nlargest(
    10,
    "nuclear_electricity"
)

fig1 = px.bar(
    top_nuclear,
    x="country",
    y="nuclear_electricity",
    color="nuclear_electricity",
    title="Top Nuclear Countries"
)

st.plotly_chart(
    fig1,
    use_container_width=True
)

# ======================================================
# TOP DECARBONISATION
# ======================================================

st.subheader("🌱 Sustainability Leaders")

leaders = latest.nlargest(
    10,
    "decarbonisation_score"
)

fig2 = px.bar(
    leaders,
    x="country",
    y="decarbonisation_score",
    color="decarbonisation_score",
    title="Top Sustainability Leaders"
)

st.plotly_chart(
    fig2,
    use_container_width=True
)

# ======================================================
# AI SUSTAINABILITY SCORE
# ======================================================

st.subheader("🌎 AI Sustainability Score")

latest["ai_score"] = (
    latest["decarbonisation_score"] * 0.5
    +
    latest["nuclear_share_elec"] * 0.3
    +
    (
        100 -
        latest["co2_per_capita_t"]
    ) * 0.2
)

top_ai = latest.nlargest(
    15,
    "ai_score"
)

fig3 = px.bar(
    top_ai,
    x="country",
    y="ai_score",
    color="ai_score",
    title="AI Sustainability Ranking"
)

st.plotly_chart(
    fig3,
    use_container_width=True
)

# ======================================================
# RISK ANALYSIS
# ======================================================

st.subheader("⚠ AI Risk Detection")

high_risk = latest[
    latest["co2_per_capita_t"]
    >
    latest["co2_per_capita_t"].quantile(0.75)
]

if len(high_risk) > 0:

    st.error(
        f"""
{len(high_risk)} countries detected with
high carbon emission risk.
"""
    )

    st.dataframe(
        high_risk[
            [
                "country",
                "co2_per_capita_t"
            ]
        ]
    )

# ======================================================
# TREND ANALYSIS
# ======================================================

st.subheader("📈 Global Trend Intelligence")

global_trend = (
    df.groupby("year")
    [
        [
            "nuclear_electricity",
            "renewables_electricity",
            "co2_per_capita_t"
        ]
    ]
    .mean()
    .reset_index()
)

fig4 = go.Figure()

fig4.add_trace(
    go.Scatter(
        x=global_trend["year"],
        y=global_trend["nuclear_electricity"],
        name="Nuclear"
    )
)

fig4.add_trace(
    go.Scatter(
        x=global_trend["year"],
        y=global_trend["renewables_electricity"],
        name="Renewables"
    )
)

fig4.update_layout(
    title="Energy Transition Trend"
)

st.plotly_chart(
    fig4,
    use_container_width=True
)

# ======================================================
# EXECUTIVE SUMMARY
# ======================================================

st.subheader("📄 Executive Summary")

summary = f"""
Analysis Year: {selected_year}

Highest Nuclear Producer:
{highest_nuclear['country']}

Highest Renewable Producer:
{highest_renewable['country']}

Lowest Carbon Country:
{lowest_carbon['country']}

Best Decarbonisation Country:
{highest_decarbon['country']}

Average Global CO₂:
{latest['co2_per_capita_t'].mean():.2f}

Average Decarbonisation Score:
{latest['decarbonisation_score'].mean():.2f}

Key Recommendation:
Increase investments in low-carbon electricity
sources and strengthen energy diversification.
"""

st.text_area(
    "AI Executive Report",
    summary,
    height=300
)

# ======================================================
# RECOMMENDATIONS
# ======================================================

st.subheader("🎯 Strategic Recommendations")

st.success("""
1. Increase low-carbon electricity generation.

2. Expand renewable energy infrastructure.

3. Maintain stable nuclear generation.

4. Improve national decarbonisation policies.

5. Reduce dependence on fossil fuels.

6. Promote energy efficiency technologies.

7. Strengthen carbon reduction initiatives.
""")

# ======================================================
# DOWNLOAD REPORT
# ======================================================

st.subheader("⬇ Download AI Report")

report_df = pd.DataFrame({
    "Metric":[
        "Highest Nuclear Producer",
        "Highest Renewable Producer",
        "Lowest Carbon Country",
        "Best Decarbonisation Country"
    ],
    "Value":[
        highest_nuclear["country"],
        highest_renewable["country"],
        lowest_carbon["country"],
        highest_decarbon["country"]
    ]
})

csv = report_df.to_csv(
    index=False
)

st.download_button(
    "Download AI Report",
    csv,
    file_name="ai_insights_report.csv",
    mime="text/csv"
)

# ======================================================
# RAW DATA
# ======================================================

with st.expander("View Dataset"):
    st.dataframe(
        latest,
        use_container_width=True
    )

st.markdown("---")

st.caption(
    "AI Insights Engine | Nuclear Energy Intelligence Dashboard"
)
