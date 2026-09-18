import pytest
from src.user_service import register_user, calculate_discount

def test_baseline_registration():
    user = register_user('john_doe', 'john@example.com')
    assert user['role'] == 'customer'
    assert user['status'] == 'active'

def test_register_user_empty_whitespace_username():
    with pytest.raises(ValueError, match="Username cannot be empty"):
        register_user("   ", "test@example.com")
    with pytest.raises(ValueError, match="Username cannot be empty"):
        register_user("", "test@example.com")

def test_register_user_invalid_email():
    with pytest.raises(ValueError, match="Invalid email format"):
        register_user("valid_user", "invalid-email-format")

def test_register_user_valid_input_trimming_defaults():
    user = register_user(" john_doe ", "john@example.com")
    assert user['username'] == "john_doe"
    assert user['email'] == "john@example.com"
    assert user['role'] == "customer"
    assert user['status'] == "active"

def test_baseline_discount():
    res = calculate_discount(100.0, 'VIP')
    assert res == 80.0
