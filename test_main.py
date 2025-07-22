import pytest
from fastapi.testclient import TestClient
from main import app, accounts


@pytest.fixture
def client():
    """Create a test client for the FastAPI app."""
    return TestClient(app)


@pytest.fixture(autouse=True)
def clear_accounts():
    """Clear the accounts dictionary before each test."""
    accounts.clear()
    yield
    accounts.clear()


class TestHealthEndpoint:
    """Test cases for the health endpoint."""
    
    def test_health_endpoint_returns_success(self, client):
        """Test that the health endpoint returns a successful status."""
        response = client.get("/healthz")
        assert response.status_code == 200
        assert response.json() == {"status": True}


class TestAccountEndpoints:
    """Test cases for account-related endpoints."""
    
    def test_get_account_not_found(self, client):
        """Test getting a non-existent account returns 404."""
        response = client.get("/accounts/1")
        assert response.status_code == 404
        assert response.json() == {"detail": "Account not found"}
    
    def test_create_account_success(self, client):
        """Test creating a new account successfully."""
        account_data = {
            "name": "Test Account",
            "description": "A test account",
            "balance": 100.0,
            "active": True
        }
        response = client.put("/accounts/1", json=account_data)
        assert response.status_code == 201
        assert response.json() == account_data
        
        # Verify the account was actually created
        get_response = client.get("/accounts/1")
        assert get_response.status_code == 200
        assert get_response.json() == account_data
    
    def test_create_account_minimal_data(self, client):
        """Test creating an account with minimal required data."""
        account_data = {
            "name": "Minimal Account",
            "balance": 50.0
        }
        response = client.put("/accounts/2", json=account_data)
        assert response.status_code == 201
        
        expected_response = {
            "name": "Minimal Account",
            "description": None,
            "balance": 50.0,
            "active": True
        }
        assert response.json() == expected_response
    
    def test_create_account_already_exists(self, client):
        """Test creating an account that already exists returns 409."""
        account_data = {
            "name": "Duplicate Account",
            "balance": 75.0
        }
        
        # Create the account first
        response1 = client.put("/accounts/3", json=account_data)
        assert response1.status_code == 201
        
        # Try to create the same account again
        response2 = client.put("/accounts/3", json=account_data)
        assert response2.status_code == 409
        assert response2.json() == {"detail": "Account exists"}
    
    def test_delete_account_success(self, client):
        """Test deleting an existing account successfully."""
        # First create an account
        account_data = {
            "name": "Account to Delete",
            "balance": 25.0
        }
        client.put("/accounts/4", json=account_data)
        
        # Verify it exists
        get_response = client.get("/accounts/4")
        assert get_response.status_code == 200
        
        # Delete the account
        delete_response = client.delete("/accounts/4")
        assert delete_response.status_code == 200
        assert delete_response.json() == {"msg": "Account deleted successfully"}
        
        # Verify it's gone
        get_response_after_delete = client.get("/accounts/4")
        assert get_response_after_delete.status_code == 404
    
    def test_delete_account_not_found(self, client):
        """Test deleting a non-existent account returns 404."""
        response = client.delete("/accounts/999")
        assert response.status_code == 404
        assert response.json() == {"detail": "Account not found"}
    
    def test_create_account_invalid_data(self, client):
        """Test creating an account with invalid data."""
        # Missing required field 'name'
        invalid_data = {
            "balance": 100.0
        }
        response = client.put("/accounts/5", json=invalid_data)
        assert response.status_code == 422  # Validation error
        
        # Invalid balance type
        invalid_data2 = {
            "name": "Invalid Account",
            "balance": "not_a_number"
        }
        response2 = client.put("/accounts/6", json=invalid_data2)
        assert response2.status_code == 422


class TestAccountsIntegration:
    """Integration tests for multiple account operations."""
    
    def test_multiple_accounts_workflow(self, client):
        """Test creating, reading, and deleting multiple accounts."""
        # Create multiple accounts
        accounts_to_create = [
            (1, {"name": "Account 1", "balance": 100.0}),
            (2, {"name": "Account 2", "balance": 200.0, "description": "Second account"}),
            (3, {"name": "Account 3", "balance": 300.0, "active": False})
        ]
        
        for account_id, account_data in accounts_to_create:
            response = client.put(f"/accounts/{account_id}", json=account_data)
            assert response.status_code == 201
        
        # Verify all accounts exist
        for account_id, expected_data in accounts_to_create:
            response = client.get(f"/accounts/{account_id}")
            assert response.status_code == 200
            
            expected_response = {
                "name": expected_data["name"],
                "description": expected_data.get("description"),
                "balance": expected_data["balance"],
                "active": expected_data.get("active", True)
            }
            assert response.json() == expected_response
        
        # Delete one account
        delete_response = client.delete("/accounts/2")
        assert delete_response.status_code == 200
        
        # Verify it's gone but others remain
        assert client.get("/accounts/2").status_code == 404
        assert client.get("/accounts/1").status_code == 200
        assert client.get("/accounts/3").status_code == 200 