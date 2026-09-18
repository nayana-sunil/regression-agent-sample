"""
Regression test suite for ADSAT-9: User Registration Validation & Role Defaults.

Each test maps 1-to-1 to a scenario in test_adsat_9_scenarios.py and is
traceable to an acceptance criterion in Jira ticket ADSAT-9.

Framework : pytest
Ticket    : ADSAT-9
"""
import pytest
from src.user_service import register_user


# ---------------------------------------------------------------------------
# AC-1: Blank / whitespace-only usernames must be rejected
# ---------------------------------------------------------------------------

class TestUsernameValidation:
    """ADSAT-9 AC-1 — register_user raises ValueError for blank usernames."""

    def test_whitespace_only_username_raises_value_error(self):
        """
        ADSAT-9-TC-01  [AC-1 | Negative]
        A username composed entirely of spaces must be rejected.
        Expected: ValueError("Username cannot be empty")
        """
        with pytest.raises(ValueError, match="Username cannot be empty"):
            register_user(username="   ", email="test@example.com")

    def test_empty_string_username_raises_value_error(self):
        """
        ADSAT-9-TC-02  [AC-1 | Negative / Edge]
        An empty-string username must be rejected.
        Expected: ValueError("Username cannot be empty")
        """
        with pytest.raises(ValueError, match="Username cannot be empty"):
            register_user(username="", email="test@example.com")


# ---------------------------------------------------------------------------
# AC-2: Emails without '@' must be rejected
# ---------------------------------------------------------------------------

class TestEmailValidation:
    """ADSAT-9 AC-2 — register_user raises ValueError for malformed emails."""

    def test_email_without_at_symbol_raises_value_error(self):
        """
        ADSAT-9-TC-03  [AC-2 | Negative]
        An email string that does not contain '@' must be rejected.
        Expected: ValueError("Invalid email format")
        """
        with pytest.raises(ValueError, match="Invalid email format"):
            register_user(username="valid_user", email="invalid-email-format")

    def test_empty_string_email_raises_value_error(self):
        """
        ADSAT-9-TC-04  [AC-2 | Negative / Edge]
        An empty-string email must also be rejected as an invalid format.
        Expected: ValueError("Invalid email format")
        """
        with pytest.raises(ValueError, match="Invalid email format"):
            register_user(username="valid_user", email="")


# ---------------------------------------------------------------------------
# AC-3: Valid inputs — whitespace trimming and default field assignment
# ---------------------------------------------------------------------------

class TestValidRegistration:
    """ADSAT-9 AC-3 — register_user trims whitespace and sets role/status defaults."""

    def test_valid_input_with_surrounding_whitespace_is_trimmed_and_defaults_set(self):
        """
        ADSAT-9-TC-05  [AC-3 | Positive]
        Leading/trailing whitespace on both username and email must be stripped.
        role must default to 'customer' and status must default to 'active'.
        """
        user = register_user(username=" john_doe ", email="john@example.com ")

        assert user["username"] == "john_doe", (
            "AC-3: username must have leading/trailing whitespace stripped"
        )
        assert user["email"] == "john@example.com", (
            "AC-3: email must have leading/trailing whitespace stripped"
        )
        assert user["role"] == "customer", (
            "AC-3: newly registered user must default to role 'customer'"
        )
        assert user["status"] == "active", (
            "AC-3: newly registered user must default to status 'active'"
        )

    def test_valid_input_without_whitespace_returns_correct_defaults(self):
        """
        ADSAT-9-TC-06  [AC-3 | Positive / Baseline]
        Clean inputs (no surrounding whitespace) must also produce the correct
        username, email, role, and status values.
        """
        user = register_user(username="jane_doe", email="jane@example.com")

        assert user["username"] == "jane_doe", (
            "AC-3: username must be preserved exactly when no whitespace is present"
        )
        assert user["email"] == "jane@example.com", (
            "AC-3: email must be preserved exactly when no whitespace is present"
        )
        assert user["role"] == "customer", (
            "AC-3: newly registered user must default to role 'customer'"
        )
        assert user["status"] == "active", (
            "AC-3: newly registered user must default to status 'active'"
        )
