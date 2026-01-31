# Portfolio Analytics Platform V3

This repository contains the third version of the Portfolio Analytics Platform — an institutional‑grade, multi‑asset analytics system built using only free data sources.  It is a complete architectural redesign of the V2 application with the following objectives:

* **Preserve analytical capabilities** from V2 (equity fundamentals, ratios, goodness score) while adding fixed income, portfolio optimisation and risk analytics.
* **Adopt modern architecture patterns** including domain‑driven design, dependency injection and repository patterns.
* **Eliminate technical debt** such as hard‑coded parameters, inconsistent sanitisation and lack of test coverage.
* **Enable rapid feature development** through modular code structure and comprehensive test suites.

## Getting Started

### Prerequisites

* Python 3.11 or higher
* Poetry or pip (see below)
* A free Yahoo Finance connection (via the `yfinance` package)

### Installation

1. Clone the repository and navigate into it:

   ```bash
   git clone <repo-url>
   cd portfolio_analytics_v3
   ```

2. Install dependencies.  We recommend using a virtual environment:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -e .[dev]
   ```

3. Copy the example environment file and populate it with your configuration:

   ```bash
   cp .env.example .env
   # Edit .env to set API keys and other settings
   ```

4. Run tests to verify your environment:

   ```bash
   make test
   ```

### Project Structure

```
portfolio_analytics_v3/
├── pyproject.toml      # Project metadata and dependencies
├── README.md           # This file
├── .env.example        # Example environment variables
├── Makefile            # Common development commands
├── docs/               # Architecture and API documentation
└── src/portfolio_analytics/
    ├── config/         # Settings and constants
    ├── domain/         # Business logic for equities, fixed income, portfolio and risk
    ├── infrastructure/ # External APIs, caching, persistence
    ├── application/    # Use‑case orchestration services
    ├── presentation/   # API, Streamlit dashboard and report generators
    └── utils/          # Sanitisation, formatting and logging utilities
```

### Development

Use the provided `Makefile` to run common tasks:

```bash
make install      # Install dependencies into the active environment
make lint         # Run ruff to lint and format code
make typecheck    # Run mypy for type checking
make test         # Run pytest
make run-api      # Run the Flask API (coming soon)
```

We follow conventional commit messages (`feat`, `fix`, `docs`, `chore`, etc.) and encourage frequent, small commits.  Pull requests should include corresponding unit tests and updates to documentation where applicable.

## Contributing

Contributions are welcome!  Please open issues for bugs or feature requests and submit pull requests against the `main` branch.  Make sure to run the test suite and linters before submitting.

## License

This project is licensed under the MIT License.  See the `LICENSE` file for details.
# portfolio-annalytics-v3
