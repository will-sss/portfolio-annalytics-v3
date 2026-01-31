# SPDX-License-Identifier: MIT

"""Entry point for the Streamlit dashboard."""

import streamlit as st  # type: ignore[import]

st.set_page_config(page_title="Portfolio Analytics Dashboard", layout="wide")

st.title("Portfolio Analytics Platform")

st.write(
    "Use the sidebar to select an analysis type and input the relevant instruments."
)

from portfolio_analytics.infrastructure.data_sources.yahoo import YahooDataSource
from portfolio_analytics.application.equity_analysis import EquityAnalysisService
from portfolio_analytics.application.bond_analysis import BondAnalysisService
from portfolio_analytics.application.portfolio_analysis import PortfolioAnalysisService
from portfolio_analytics.domain.portfolio.models import Holding, Portfolio
from portfolio_analytics.domain.common.models import Instrument
import plotly.graph_objects as go  # type: ignore[import]
import numpy as np  # type: ignore[import]
from portfolio_analytics.domain.risk import (
    historical_var,
    parametric_var,
    monte_carlo_var,
    max_drawdown,
    correlation_matrix,
)


def equity_page() -> None:
    """Interactive equity analysis page."""
    st.header("Equity Analysis")
    tickers_input = st.text_input(
        "Enter comma‑separated tickers", value="AAPL, MSFT, GOOGL"
    )
    analyse = st.button("Analyse Equities")
    if analyse:
        tickers = [t.strip().upper() for t in tickers_input.split(",") if t.strip()]
        ds = YahooDataSource()
        service = EquityAnalysisService(ds)
        results = []
        for t in tickers:
            try:
                res = service.analyse(t)
                results.append(res)
            except Exception as exc:
                st.error(f"Error analysing {t}: {exc}")
        if results:
            # Display fundamentals and ratios as tables
            fundamentals_rows = []
            valuations_rows = []
            for res in results:
                fundamentals = res.get("fundamentals", {})
                ratios = res.get("ratios", {})
                valuation = res.get("valuation", {})
                fundamentals_rows.append(
                    {
                        "Ticker": fundamentals.get("equity", {}).get("symbol"),
                        "Name": fundamentals.get("equity", {}).get("name"),
                        "Sector": fundamentals.get("equity", {}).get("sector"),
                        "Rev CAGR": fundamentals.get("revenue_cagr"),
                        "Net Margin": fundamentals.get("net_margin"),
                        "Operating Margin": fundamentals.get("operating_margin"),
                        "CFO/NI": fundamentals.get("cfo_to_ni"),
                        "Leverage": fundamentals.get("leverage_ratio"),
                    }
                )
                valuations_rows.append(
                    {
                        "Ticker": valuation.get("equity", {}).get("symbol"),
                        "Actual P/E": valuation.get("actual_pe"),
                        "Expected P/E": valuation.get("expected_pe"),
                        "Status": valuation.get("status"),
                    }
                )
            st.subheader("Fundamentals")
            st.dataframe(fundamentals_rows)
            st.subheader("Valuation")
            st.dataframe(valuations_rows)
            # Plot actual vs expected P/E
            pe_actual = [row["Actual P/E"] for row in valuations_rows]
            pe_expected = [row["Expected P/E"] for row in valuations_rows]
            labels = [row["Ticker"] for row in valuations_rows]
            fig = go.Figure()
            fig.add_trace(
                go.Bar(name="Actual P/E", x=labels, y=pe_actual, marker_color="blue")
            )
            fig.add_trace(
                go.Bar(name="Expected P/E", x=labels, y=pe_expected, marker_color="orange")
            )
            fig.update_layout(
                title="Actual vs Expected P/E", barmode="group", xaxis_title="Ticker", yaxis_title="P/E"
            )
            st.plotly_chart(fig, use_container_width=True)


def bond_page() -> None:
    """Interactive bond analysis page (placeholder)."""
    st.header("Bond Analysis")
    st.write("Bond analysis is not yet implemented for the free Yahoo data source.")


def portfolio_page() -> None:
    """Interactive portfolio analysis page."""
    st.header("Portfolio Analysis")
    st.write("Enter your holdings below.  For demonstration purposes, synthetic risk metrics will be generated.")
    n = st.number_input("Number of holdings", min_value=1, max_value=20, value=3, step=1)
    holdings = []
    for i in range(int(n)):
        col1, col2 = st.columns(2)
        with col1:
            symbol = st.text_input(f"Instrument {i+1} symbol", key=f"sym_{i}", value="AAPL")
        with col2:
            qty = st.number_input(f"Quantity {i+1}", key=f"qty_{i}", value=100.0)
        holdings.append({"instrument": {"symbol": symbol}, "quantity": qty})
    analyse = st.button("Analyse Portfolio")
    if analyse:
        ds = YahooDataSource()
        service = PortfolioAnalysisService(ds)
        try:
            # Build Portfolio and analyse
            instruments = []
            inst_objs = []
            for h in holdings:
                inst_objs.append(Instrument(symbol=h["instrument"]["symbol"]))
            # In this simplified UI, we rely on the service to handle conversions
            portfolio = Portfolio(
                holdings=[Holding(instrument=Instrument(symbol=h["instrument"]["symbol"]), quantity=h["quantity"]) for h in holdings]
            )
            result = service.analyse(portfolio)
            st.subheader("Portfolio Summary")
            st.json(result)
            if "correlation_matrix" in result:
                corr = result["correlation_matrix"]
                fig = go.Figure(data=go.Heatmap(z=corr, x=[h["instrument"]["symbol"] for h in holdings], y=[h["instrument"]["symbol"] for h in holdings], colorscale="Viridis"))
                fig.update_layout(title="Correlation Matrix", xaxis_title="Instrument", yaxis_title="Instrument")
                st.plotly_chart(fig, use_container_width=True)
        except Exception as exc:
            st.error(f"Error analysing portfolio: {exc}")


def risk_page() -> None:
    """Interactive risk analysis page.

    Users can input one or more return series as comma‑separated values (one
    series per line).  The page computes historical, parametric and
    Monte Carlo VaR at the 95% confidence level, maximum drawdown and
    pairwise correlations.  Simple charts display the return distribution
    and correlation matrix.
    """
    st.header("Risk Analysis")
    st.write(
        "Enter return series as comma‑separated values.  For multiple series, enter one series per line."
    )
    data_input = st.text_area(
        "Return series", height=200, placeholder="0.01, -0.02, 0.015\n0.005, -0.01, 0.02"
    )
    analyse = st.button("Compute Risk Metrics")
    if analyse:
        if not data_input.strip():
            st.warning("Please enter at least one series of returns.")
            return
        # Parse input lines into lists of floats
        series = []
        for line in data_input.strip().splitlines():
            try:
                values = [float(x.strip()) for x in line.split(",") if x.strip()]
                if values:
                    series.append(values)
            except ValueError:
                st.error(f"Invalid number in line: {line}")
                return
        # Ensure equal lengths by padding shorter series with nan and dropping nan values later
        max_len = max(len(s) for s in series)
        padded = []
        for s in series:
            if len(s) < max_len:
                s = s + [np.nan] * (max_len - len(s))  # type: ignore[name-defined]
            padded.append(s)
        # Convert to numpy array
        arr = np.array(padded, dtype=float)
        # Remove rows with nan at the end (if any)
        arr = np.where(np.isnan(arr), np.nan, arr)
        # Compute portfolio risk metrics for each series individually and overall correlation
        var_results = []
        drawdown_results = []
        for idx, s in enumerate(arr):
            # Remove nan values for this series
            clean = s[~np.isnan(s)]
            if clean.size == 0:
                continue
            h_var = historical_var(clean, 0.95)
            p_var = parametric_var(clean, 0.95)
            mc_var = monte_carlo_var(clean, 0.95, 5000)
            max_dd, dd_start, dd_end, dd_rec = max_drawdown(clean.tolist())
            var_results.append(
                {
                    "Series": f"Series {idx+1}",
                    "Historical VaR": h_var,
                    "Parametric VaR": p_var,
                    "Monte Carlo VaR": mc_var,
                    "Max Drawdown": max_dd,
                }
            )
            drawdown_results.append(max_dd)
        st.subheader("VaR and Drawdown")
        st.table(var_results)
        # Correlation matrix if more than one series
        if len(series) > 1:
            # Use padded array for correlation; fill nan with zeros
            arr_filled = np.nan_to_num(arr)
            corr = correlation_matrix(arr_filled)
            fig = go.Figure(
                data=go.Heatmap(
                    z=corr, x=[f"S{i+1}" for i in range(len(series))], y=[f"S{i+1}" for i in range(len(series))], colorscale="RdBu", zmin=-1, zmax=1
                )
            )
            fig.update_layout(title="Correlation Matrix", xaxis_title="Series", yaxis_title="Series")
            st.plotly_chart(fig, use_container_width=True)
        # Distribution plot for first series
        if series:
            clean = np.array(series[0], dtype=float)
            clean = clean[~np.isnan(clean)]
            hist_fig = go.Figure(
                data=[go.Histogram(x=clean, nbinsx=20, marker_color="green")],
                layout_title_text="Return Distribution (Series 1)"
            )
            st.plotly_chart(hist_fig, use_container_width=True)


def main() -> None:
    # Sidebar navigation
    section = st.sidebar.selectbox(
        "Select analysis", ["Equity", "Bond", "Portfolio", "Risk"], index=0
    )
    if section == "Equity":
        equity_page()
    elif section == "Bond":
        bond_page()
    elif section == "Portfolio":
        portfolio_page()
    elif section == "Risk":
        risk_page()


if __name__ == "__main__":
    main()
