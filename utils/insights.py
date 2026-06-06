import pandas as pd
import numpy as np


# ==========================================================
# HIGHEST NUCLEAR PRODUCER
# ==========================================================

def highest_nuclear_producer(df):

    row = df.loc[
        df["nuclear_electricity"].idxmax()
    ]

    return {
        "country": row["country"],
        "value": row["nuclear_electricity"]
    }


# ==========================================================
# HIGHEST RENEWABLE PRODUCER
# ==========================================================

def highest_renewable_producer(df):

    row = df.loc[
        df["renewables_electricity"].idxmax()
    ]

    return {
        "country": row["country"],
        "value": row["renewables_electricity"]
    }


# ==========================================================
# LOWEST CO2 COUNTRY
# ==========================================================

def lowest_carbon_country(df):

    row = df.loc[
        df["co2_per_capita_t"].idxmin()
    ]

    return {
        "country": row["country"],
        "value": row["co2_per_capita_t"]
    }


# ==========================================================
# HIGHEST CO2 COUNTRY
# ==========================================================

def highest_carbon_country(df):

    row = df.loc[
        df["co2_per_capita_t"].idxmax()
    ]

    return {
        "country": row["country"],
        "value": row["co2_per_capita_t"]
    }


# ==========================================================
# BEST DECARBONISATION COUNTRY
# ==========================================================

def best_decarbonisation_country(df):

    row = df.loc[
        df["decarbonisation_score"].idxmax()
    ]

    return {
        "country": row["country"],
        "value": row["decarbonisation_score"]
    }


# ==========================================================
# WORST DECARBONISATION COUNTRY
# ==========================================================

def worst_decarbonisation_country(df):

    row = df.loc[
        df["decarbonisation_score"].idxmin()
    ]

    return {
        "country": row["country"],
        "value": row["decarbonisation_score"]
    }


# ==========================================================
# AI SUSTAINABILITY SCORE
# ==========================================================

def calculate_ai_score(df):

    temp = df.copy()

    temp["ai_score"] = (
        temp["decarbonisation_score"] * 0.50
        +
        temp["nuclear_share_elec"] * 0.30
        +
        (100 - temp["co2_per_capita_t"]) * 0.20
    )

    return temp


# ==========================================================
# TOP AI COUNTRIES
# ==========================================================

def top_ai_countries(df, n=10):

    temp = calculate_ai_score(df)

    return temp.nlargest(
        n,
        "ai_score"
    )


# ==========================================================
# HIGH RISK COUNTRIES
# ==========================================================

def high_risk_countries(df):

    threshold = df[
        "co2_per_capita_t"
    ].quantile(0.75)

    return df[
        df["co2_per_capita_t"] >= threshold
    ]


# ==========================================================
# LOW RISK COUNTRIES
# ==========================================================

def low_risk_countries(df):

    threshold = df[
        "co2_per_capita_t"
    ].quantile(0.25)

    return df[
        df["co2_per_capita_t"] <= threshold
    ]


# ==========================================================
# GLOBAL SUMMARY
# ==========================================================

def global_summary(df):

    summary = {

        "countries":
        df["country"].nunique(),

        "years":
        df["year"].nunique(),

        "total_nuclear":
        round(
            df["nuclear_electricity"].sum(),
            2
        ),

        "total_renewables":
        round(
            df["renewables_electricity"].sum(),
            2
        ),

        "avg_co2":
        round(
            df["co2_per_capita_t"].mean(),
            2
        ),

        "avg_decarbonisation":
        round(
            df["decarbonisation_score"].mean(),
            2
        )
    }

    return summary


# ==========================================================
# NUCLEAR INSIGHTS
# ==========================================================

def nuclear_insights(df):

    leader = highest_nuclear_producer(df)

    return f"""
Highest Nuclear Producer:
{leader['country']}

Production:
{leader['value']:,.2f}
"""


# ==========================================================
# RENEWABLE INSIGHTS
# ==========================================================

def renewable_insights(df):

    leader = highest_renewable_producer(df)

    return f"""
Highest Renewable Producer:
{leader['country']}

Production:
{leader['value']:,.2f}
"""


# ==========================================================
# CARBON INSIGHTS
# ==========================================================

def carbon_insights(df):

    low = lowest_carbon_country(df)

    high = highest_carbon_country(df)

    return f"""
Lowest Carbon Country:
{low['country']} ({low['value']:.2f})

Highest Carbon Country:
{high['country']} ({high['value']:.2f})
"""


# ==========================================================
# DECARBONISATION INSIGHTS
# ==========================================================

def decarbonisation_insights(df):

    best = best_decarbonisation_country(df)

    return f"""
Best Decarbonisation Country:
{best['country']}

Score:
{best['value']:.2f}
"""


# ==========================================================
# COUNTRY REPORT
# ==========================================================

def country_report(df, country):

    data = df[
        df["country"] == country
    ]

    latest = data.sort_values(
        "year"
    ).iloc[-1]

    report = f"""
Country: {country}

Year:
{latest['year']}

Nuclear Electricity:
{latest['nuclear_electricity']:,.2f}

Renewables Electricity:
{latest['renewables_electricity']:,.2f}

CO2 Per Capita:
{latest['co2_per_capita_t']:.2f}

Decarbonisation Score:
{latest['decarbonisation_score']:.2f}
"""

    return report


# ==========================================================
# EXECUTIVE SUMMARY
# ==========================================================

def executive_summary(df):

    nuclear = highest_nuclear_producer(df)
    renewable = highest_renewable_producer(df)
    carbon = lowest_carbon_country(df)
    decarb = best_decarbonisation_country(df)

    summary = f"""
EXECUTIVE ENERGY REPORT

Highest Nuclear Producer:
{nuclear['country']}

Highest Renewable Producer:
{renewable['country']}

Lowest Carbon Country:
{carbon['country']}

Best Decarbonisation Country:
{decarb['country']}

Strategic Recommendations:

1. Increase low-carbon electricity generation.
2. Expand renewable energy deployment.
3. Maintain safe nuclear energy growth.
4. Improve carbon reduction initiatives.
5. Strengthen sustainability policies.
"""

    return summary


# ==========================================================
# RECOMMENDATIONS ENGINE
# ==========================================================

def generate_recommendations(df):

    recommendations = []

    avg_co2 = df[
        "co2_per_capita_t"
    ].mean()

    avg_nuclear = df[
        "nuclear_share_elec"
    ].mean()

    if avg_co2 > 5:
        recommendations.append(
            "Reduce carbon emissions through low-carbon energy expansion."
        )

    if avg_nuclear < 20:
        recommendations.append(
            "Increase nuclear electricity share where feasible."
        )

    recommendations.append(
        "Expand renewable energy infrastructure."
    )

    recommendations.append(
        "Improve energy efficiency programs."
    )

    recommendations.append(
        "Support long-term decarbonisation strategies."
    )

    return recommendations


# ==========================================================
# AI DASHBOARD CARDS
# ==========================================================

def dashboard_cards(df):

    return {
        "highest_nuclear":
            highest_nuclear_producer(df),

        "highest_renewable":
            highest_renewable_producer(df),

        "lowest_carbon":
            lowest_carbon_country(df),

        "best_decarbonisation":
            best_decarbonisation_country(df)
    }
