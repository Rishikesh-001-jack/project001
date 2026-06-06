import plotly.express as px
import plotly.graph_objects as go
import pandas as pd


# ==========================================================
# GLOBAL LINE CHART
# ==========================================================

def line_chart(
    df,
    x_col,
    y_col,
    title,
    color=None
):
    fig = px.line(
        df,
        x=x_col,
        y=y_col,
        color=color,
        markers=True,
        title=title
    )

    fig.update_layout(
        template="plotly_white",
        height=500
    )

    return fig


# ==========================================================
# AREA CHART
# ==========================================================

def area_chart(
    df,
    x_col,
    y_col,
    title
):
    fig = px.area(
        df,
        x=x_col,
        y=y_col,
        title=title
    )

    fig.update_layout(
        template="plotly_white",
        height=500
    )

    return fig


# ==========================================================
# BAR CHART
# ==========================================================

def bar_chart(
    df,
    x_col,
    y_col,
    title,
    color_col=None
):
    fig = px.bar(
        df,
        x=x_col,
        y=y_col,
        color=color_col,
        text_auto=True,
        title=title
    )

    fig.update_layout(
        template="plotly_white",
        height=500
    )

    return fig


# ==========================================================
# HORIZONTAL BAR CHART
# ==========================================================

def horizontal_bar_chart(
    df,
    x_col,
    y_col,
    title,
    color_col=None
):
    fig = px.bar(
        df,
        x=x_col,
        y=y_col,
        orientation="h",
        color=color_col,
        title=title
    )

    fig.update_layout(
        template="plotly_white",
        height=600
    )

    return fig


# ==========================================================
# PIE CHART
# ==========================================================

def pie_chart(
    df,
    names_col,
    values_col,
    title
):
    fig = px.pie(
        df,
        names=names_col,
        values=values_col,
        hole=0.5,
        title=title
    )

    fig.update_layout(
        height=500
    )

    return fig


# ==========================================================
# DONUT CHART
# ==========================================================

def donut_chart(
    df,
    names_col,
    values_col,
    title
):
    fig = px.pie(
        df,
        names=names_col,
        values=values_col,
        hole=0.65,
        title=title
    )

    return fig


# ==========================================================
# SCATTER CHART
# ==========================================================

def scatter_chart(
    df,
    x_col,
    y_col,
    title,
    color_col=None,
    size_col=None,
    hover_col=None
):
    fig = px.scatter(
        df,
        x=x_col,
        y=y_col,
        color=color_col,
        size=size_col,
        hover_name=hover_col,
        title=title
    )

    fig.update_layout(
        template="plotly_white",
        height=550
    )

    return fig


# ==========================================================
# BUBBLE CHART
# ==========================================================

def bubble_chart(
    df,
    x_col,
    y_col,
    size_col,
    color_col,
    hover_col,
    title
):
    fig = px.scatter(
        df,
        x=x_col,
        y=y_col,
        size=size_col,
        color=color_col,
        hover_name=hover_col,
        title=title
    )

    return fig


# ==========================================================
# HISTOGRAM
# ==========================================================

def histogram_chart(
    df,
    column,
    title
):
    fig = px.histogram(
        df,
        x=column,
        nbins=30,
        title=title
    )

    fig.update_layout(
        template="plotly_white"
    )

    return fig


# ==========================================================
# BOX PLOT
# ==========================================================

def box_plot(
    df,
    x_col,
    y_col,
    title
):
    fig = px.box(
        df,
        x=x_col,
        y=y_col,
        title=title
    )

    return fig


# ==========================================================
# VIOLIN PLOT
# ==========================================================

def violin_plot(
    df,
    x_col,
    y_col,
    title
):
    fig = px.violin(
        df,
        x=x_col,
        y=y_col,
        box=True,
        points="all",
        title=title
    )

    return fig


# ==========================================================
# MULTI LINE CHART
# ==========================================================

def multi_line_chart(
    df,
    x_col,
    y_cols,
    title
):
    fig = px.line(
        df,
        x=x_col,
        y=y_cols,
        markers=True,
        title=title
    )

    fig.update_layout(
        template="plotly_white",
        height=550
    )

    return fig


# ==========================================================
# TOP N RANKING
# ==========================================================

def top_n_bar(
    df,
    column,
    n=10,
    title="Top Ranking"
):
    top_df = df.nlargest(
        n,
        column
    )

    fig = px.bar(
        top_df,
        x="country",
        y=column,
        color=column,
        title=title
    )

    return fig


# ==========================================================
# BOTTOM N RANKING
# ==========================================================

def bottom_n_bar(
    df,
    column,
    n=10,
    title="Bottom Ranking"
):
    low_df = df.nsmallest(
        n,
        column
    )

    fig = px.bar(
        low_df,
        x="country",
        y=column,
        color=column,
        title=title
    )

    return fig


# ==========================================================
# FORECAST CHART
# ==========================================================

def forecast_chart(
    historical_df,
    future_df,
    x_col,
    historical_col,
    forecast_col,
    title
):
    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=historical_df[x_col],
            y=historical_df[historical_col],
            mode="lines",
            name="Historical"
        )
    )

    fig.add_trace(
        go.Scatter(
            x=future_df[x_col],
            y=future_df[forecast_col],
            mode="lines+markers",
            name="Forecast"
        )
    )

    fig.update_layout(
        title=title,
        template="plotly_white",
        height=550
    )

    return fig


# ==========================================================
# KPI HELPER
# ==========================================================

def calculate_kpis(df):

    kpis = {
        "countries":
            df["country"].nunique(),

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


# ==========================================================
# ENERGY MIX DATAFRAME
# ==========================================================

def energy_mix_dataframe(df):

    return pd.DataFrame({
        "Source": [
            "Nuclear",
            "Renewables"
        ],
        "Value": [
            df["nuclear_electricity"].sum(),
            df["renewables_electricity"].sum()
        ]
    })
