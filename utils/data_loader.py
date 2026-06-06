import pandas as pd
import streamlit as st


# =====================================================
# LOAD DATASET
# =====================================================

@st.cache_data
def load_data(
    file_path="data/global_nuclear_energy_intelligence_1965_2025.csv"
):
    """
    Load dataset and cache it.
    """

    df = pd.read_csv(file_path)

    return df


# =====================================================
# CLEAN DATA
# =====================================================

def clean_data(df):
    """
    Basic data cleaning.
    """

    df = df.copy()

    # Remove duplicate rows
    df.drop_duplicates(inplace=True)

    # Standardize column names
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
    )

    return df


# =====================================================
# HANDLE MISSING VALUES
# =====================================================

def handle_missing_values(df):
    """
    Fill missing numeric values with median.
    Fill missing categorical values with Unknown.
    """

    df = df.copy()

    numeric_cols = df.select_dtypes(
        include=["int64", "float64"]
    ).columns

    categorical_cols = df.select_dtypes(
        include=["object"]
    ).columns

    for col in numeric_cols:
        df[col] = df[col].fillna(
            df[col].median()
        )

    for col in categorical_cols:
        df[col] = df[col].fillna(
            "Unknown"
        )

    return df


# =====================================================
# CONVERT NUMERIC COLUMNS
# =====================================================

def convert_numeric_columns(df):

    df = df.copy()

    for col in df.columns:

        try:
            df[col] = pd.to_numeric(
                df[col]
            )
        except:
            pass

    return df


# =====================================================
# FULL PREPROCESSING PIPELINE
# =====================================================

def preprocess_data(df):

    df = clean_data(df)

    df = handle_missing_values(df)

    df = convert_numeric_columns(df)

    return df


# =====================================================
# GET AVAILABLE COUNTRIES
# =====================================================

def get_countries(df):

    return sorted(
        df["country"]
        .dropna()
        .unique()
        .tolist()
    )


# =====================================================
# FILTER COUNTRY
# =====================================================

def filter_country(
    df,
    country
):

    return df[
        df["country"] == country
    ]


# =====================================================
# FILTER MULTIPLE COUNTRIES
# =====================================================

def filter_countries(
    df,
    countries
):

    return df[
        df["country"].isin(countries)
    ]


# =====================================================
# FILTER YEAR RANGE
# =====================================================

def filter_year_range(
    df,
    start_year,
    end_year
):

    return df[
        (df["year"] >= start_year)
        &
        (df["year"] <= end_year)
    ]


# =====================================================
# FILTER COUNTRY + YEAR
# =====================================================

def filter_country_year(
    df,
    country,
    start_year,
    end_year
):

    filtered = df[
        (df["country"] == country)
        &
        (df["year"] >= start_year)
        &
        (df["year"] <= end_year)
    ]

    return filtered


# =====================================================
# GET LATEST YEAR DATA
# =====================================================

def latest_year_data(df):

    latest_year = df["year"].max()

    return df[
        df["year"] == latest_year
    ]


# =====================================================
# KPI CALCULATOR
# =====================================================

def calculate_kpis(df):

    kpis = {

        "countries":
        df["country"].nunique(),

        "latest_year":
        int(df["year"].max()),

        "total_nuclear":
        df["nuclear_electricity"].sum(),

        "total_renewables":
        df["renewables_electricity"].sum(),

        "avg_co2":
        df["co2_per_capita_t"].mean(),

        "avg_decarbonisation":
        df["decarbonisation_score"].mean()
    }

    return kpis


# =====================================================
# TOP COUNTRIES
# =====================================================

def get_top_countries(
    df,
    metric,
    n=10
):

    return df.nlargest(
        n,
        metric
    )


# =====================================================
# BOTTOM COUNTRIES
# =====================================================

def get_bottom_countries(
    df,
    metric,
    n=10
):

    return df.nsmallest(
        n,
        metric
    )


# =====================================================
# GLOBAL YEARLY TREND
# =====================================================

def global_yearly_trend(
    df,
    metric
):

    trend = (
        df.groupby("year")[metric]
        .sum()
        .reset_index()
    )

    return trend


# =====================================================
# COUNTRY YEARLY TREND
# =====================================================

def country_yearly_trend(
    df,
    country,
    metric
):

    trend = (
        df[
            df["country"] == country
        ]
        .groupby("year")[metric]
        .sum()
        .reset_index()
    )

    return trend


# =====================================================
# ENERGY MIX DATA
# =====================================================

def energy_mix_data(df):

    return pd.DataFrame({

        "Source": [
            "Nuclear",
            "Renewables"
        ],

        "Value": [

            df[
                "nuclear_electricity"
            ].sum(),

            df[
                "renewables_electricity"
            ].sum()
        ]
    })


# =====================================================
# DOWNLOAD CSV
# =====================================================

def dataframe_to_csv(df):

    return df.to_csv(
        index=False
    ).encode("utf-8")


# =====================================================
# DATASET SUMMARY
# =====================================================

def dataset_summary(df):

    summary = {

        "Rows":
        df.shape[0],

        "Columns":
        df.shape[1],

        "Countries":
        df["country"].nunique(),

        "Start Year":
        df["year"].min(),

        "End Year":
        df["year"].max()
    }

    return summary


# =====================================================
# FEATURE LIST
# =====================================================

def numeric_features(df):

    return df.select_dtypes(
        include=["int64", "float64"]
    ).columns.tolist()


# =====================================================
# CORRELATION MATRIX
# =====================================================

def correlation_matrix(df):

    numeric_df = df.select_dtypes(
        include=["int64", "float64"]
    )

    return numeric_df.corr()


# =====================================================
# LOAD AND PREPROCESS
# =====================================================

@st.cache_data
def load_and_prepare_data():

    df = load_data()

    df = preprocess_data(df)

    return df
