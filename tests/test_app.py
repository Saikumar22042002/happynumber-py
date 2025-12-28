"""
Unit tests for the Happy Number Flask application.
Ensures that all endpoints and logic function as expected.
"""
import pytest
from app import app as flask_app  # Use an alias to avoid Pylint warnings


@pytest.fixture(scope="module")
def app():
    """Provides a test instance of the Flask application."""
    # pylint: disable=redefined-outer-name
    flask_app.config.update({"TESTING": True})
    yield flask_app


@pytest.fixture(scope="module")
def client(app):
    """Provides a test client for the Flask application."""
    return app.test_client()


def test_health_check(client):
    """Test the /health endpoint for a successful response."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json == {"status": "healthy"}


def test_index_endpoint(client):
    """Test the index endpoint for a welcome message."""
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json


@pytest.mark.parametrize(
    "number, expected_status, expected_happy",
    [
        (7, 200, True),  # A known happy number
        (19, 200, True),  # Another known happy number
        (4, 200, False),  # A known unhappy number (enters a cycle)
        (1, 200, True),  # The base case for happy numbers
    ],
)
def test_is_happy_endpoint(client, number, expected_status, expected_happy):
    """Test the /is_happy/<number> endpoint with various valid numbers."""
    response = client.get(f"/is_happy/{number}")
    assert response.status_code == expected_status
    assert response.json == {"number": number, "is_happy": expected_happy}


@pytest.mark.parametrize(
    "number, expected_status, expected_error",
    [
        (0, 400, "Number must be a positive integer."),
        (-5, 400, "Number must be a positive integer."),
    ],
)
def test_is_happy_invalid_input(client, number, expected_status, expected_error):
    """Test the /is_happy endpoint with invalid (non-positive) numbers."""
    response = client.get(f"/is_happy/{number}")
    assert response.status_code == expected_status
    assert response.json == {"error": expected_error}


def test_is_happy_non_integer_path(client):
    """Test that a non-integer path parameter results in a 404 Not Found."""
    response = client.get("/is_happy/not-a-number")
    assert response.status_code == 404
