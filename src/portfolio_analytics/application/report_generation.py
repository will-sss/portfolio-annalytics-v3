# SPDX-License-Identifier: MIT

"""Service for generating reports from analysis results."""

from __future__ import annotations

import logging
from typing import Dict, Any

from ..config.settings import Settings, settings
from ..utils.sanitization import to_serializable


logger = logging.getLogger(__name__)


class ReportGenerationService:
    """Generate HTML reports based on analysis results."""

    def __init__(self, cfg: Settings | None = None) -> None:
        self.cfg = cfg or settings

    def generate_equity_report(self, analysis: Dict[str, Any]) -> str:
        """Generate an HTML report from equity analysis results.

        The report includes a summary section, fundamentals table and
        valuation comparison.  Plotly charts could be embedded in
        future versions by converting them to HTML fragments.

        Parameters
        ----------
        analysis:
            A dictionary produced by :class:`EquityAnalysisService` for a
            single ticker.

        Returns
        -------
        str
            A complete HTML report.
        """
        logger.info("Generating equity report")
        from ..presentation.reports.html_generator import build_html_report

        fundamentals = analysis.get("fundamentals", {})
        ratios = analysis.get("ratios", {})
        valuation = analysis.get("valuation", {})
        equity_info = fundamentals.get("equity", {})
        symbol = equity_info.get("symbol", "")

        # Build summary section
        summary_html = f"""
        <p><strong>Company:</strong> {equity_info.get('name', '')}</p>
        <p><strong>Ticker:</strong> {symbol}</p>
        <p><strong>Sector:</strong> {equity_info.get('sector', '')}</p>
        """
        # Fundamentals table
        fundamentals_rows = [
            ("Revenue CAGR", fundamentals.get("revenue_cagr")),
            ("Net Margin", fundamentals.get("net_margin")),
            ("Operating Margin", fundamentals.get("operating_margin")),
            ("CFO/NI", fundamentals.get("cfo_to_ni")),
            ("Leverage", fundamentals.get("leverage_ratio")),
            ("Lifecycle", fundamentals.get("lifecycle")),
        ]
        fundamentals_html = "<table>" + "".join(
            f"<tr><td>{name}</td><td>{value:.4f if isinstance(value, (int, float)) else value}</td></tr>"
            for name, value in fundamentals_rows
        ) + "</table>"
        # Valuation comparison
        valuation_html = f"""
        <table>
          <tr><th>Metric</th><th>Value</th></tr>
          <tr><td>Actual P/E</td><td>{valuation.get('actual_pe')}</td></tr>
          <tr><td>Expected P/E</td><td>{valuation.get('expected_pe')}</td></tr>
          <tr><td>Status</td><td>{valuation.get('status')}</td></tr>
        </table>
        """
        sections = {
            "Summary": summary_html,
            "Fundamentals": fundamentals_html,
            "Valuation": valuation_html,
        }
        title = f"Equity Analysis Report: {symbol}"
        return build_html_report(title, sections)
