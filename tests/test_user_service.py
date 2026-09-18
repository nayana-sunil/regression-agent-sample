import pytest
from src.user_service import register_user, calculate_discount

def test_baseline_registration():
    user = register_user('john_doe', 'john@example.com')
    assert user['role'] == 'customer'

def test_baseline_discount():
    res = calculate_discount(100.0, 'VIP')
    assert res == 80.0
