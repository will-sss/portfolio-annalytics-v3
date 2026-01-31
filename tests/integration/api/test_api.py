"""Integration tests for Flask API endpoints."""

from portfolio_analytics.presentation.api.app import create_app


def test_health_endpoint() -> None:
    """Ensure the health endpoint returns a 200 OK response."""
    app = create_app()
    client = app.test_client()
    response = client.get("/health")
    assert response.status_code == 200
    data = response.get_json()
    assert data == {"status": "ok"}