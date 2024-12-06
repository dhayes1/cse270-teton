import pytest
import responses
import requests

# Define the base URL for the mock server
BASE_URL = "http://127.0.0.1:8000/users"

@pytest.fixture
def mock_server():
    with responses.RequestsMock() as rsps:
        # Mock the unauthorized response
        rsps.add(
            method=responses.GET,
            url=BASE_URL,
            match=[responses.matchers.query_param_matcher({"username": "admin", "password": "admin"})],
            status=401,
            body=""
        )
        
        # Mock the authorized response with an empty body
        rsps.add(
            method=responses.GET,
            url=BASE_URL,
            match=[responses.matchers.query_param_matcher({"username": "admin", "password": "qwerty"})],
            status=200,
            body=""
        )
        
        yield rsps


def test_users_endpoint_unauthorized(mock_server):
    # Define the parameters
    params = {"username": "admin", "password": "admin"}
    
    # Send the GET request
    response = requests.get(BASE_URL, params=params)
    
    # Assert the HTTP status code is 401
    assert response.status_code == 401, f"Expected 401, got {response.status_code}"
    
    # Assert the response body is empty
    assert response.text.strip() == "", f"Expected empty response, got: {response.text}"


def test_users_endpoint_success_with_empty_response(mock_server):
    # Define the parameters
    params = {"username": "admin", "password": "qwerty"}
    
    # Send the GET request
    response = requests.get(BASE_URL, params=params)
    
    # Assert the HTTP status code is 200
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    
    # Assert the response body is empty
    assert response.text.strip() == "", f"Expected empty response, got: {response.text}"
