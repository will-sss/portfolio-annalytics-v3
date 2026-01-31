# Quality Assurance Plan

This document outlines the plan for validating and testing the Portfolio Analytics
Platform V3.  It describes the types of tests to be written, the target
coverage levels and the parity validation approach against V2.

## Unit Testing

- **Coverage Target:** 90 % for new domain logic and utilities.
- **Scope:**
  - Risk analytics functions (VaR, drawdown, correlation)
  - Portfolio rebalancing and simulation utilities
  - Sanitisation and formatting utilities
  - Domain model validation rules
- **Tools:** `pytest`, with fixtures for sample data.

## Integration Testing

- **API Endpoints:** Use Flask's test client to verify that health checks and
  analysis endpoints return expected status codes and basic responses.
- **Data Source Adapters:** Mock external API calls to test the Yahoo
  adapter’s handling of missing data, rate limiting and error conditions.

## Parity Validation

- A script (``scripts/validate_parity.py``) will be implemented to run
  equivalent analyses in both V2 and V3, comparing outputs for numerical
  accuracy.  Discrepancies will be logged and investigated.

## Continuous Integration

- Configure a CI pipeline to run `pytest` with coverage reports and
  enforce linting with ruff and type checking with mypy.
