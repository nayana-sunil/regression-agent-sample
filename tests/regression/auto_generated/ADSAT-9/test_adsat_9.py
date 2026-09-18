"""Regression tests for ADSAT-9: User Registration Validation & Role Defaults.

Each test maps 1-to-1 to a named scenario in test_adsat_9.md.
Source of truth: Jira ticket ADSAT-9 (Knowledge Base).
"""
import pytest
from src.user_service import register_user


# ---------------------------------------------------------------------------
# Acceptance Criterion 1 — Blank / whitespace-only username is rejected
# ---------------------------------------------------------------------------

class TestUsernameValidation:
    """ADSAT-9 AC-1: register_user must reject blank or whitespace-only usernames."""

    def test_whitespace_only_username_raises_value_error(self):
        """Scenario 1.1 — Whitespace-only username raises ValueError.

        Requirement: ADSAT-9 AC-1
        A username composed entirely of spaces must be rejected with the
        exact message 'Username cannot be empty'.
        """
        with pytest.raises(ValueError, match="Username cannot be empty"):
            register_user(username="   ", email="test@example.com")

    def test_empty_string_username_raises_value_error(self):
        """Scenario 1.2 — Empty-string username raises ValueError (edge case).

        Requirement: ADSAT-9 AC-1
        A zero-length username string must be rejected with the exact message
        'Username cannot be empty'.
        """
        with pytest.raises(ValueError, match="Username cannot be empty"):
            register_user(username="", email="test@example.com")

    def test_valid_username_does_not_raise(self):
        """Scenario 1.3 — Valid username does NOT raise ValueError (no false positive).

        Requirement: ADSAT-9 AC-1
        A non-blank username must not trigger the username validation error;
        the function must return a dict successfully.
        """
        result = register_user(username="valid_user", email="valid@example.com")
        assert isinstance(result, dict), (
            "register_user should return a dict for valid inputs, not raise an exception."
        )


# ---------------------------------------------------------------------------
# Acceptance Criterion 2 — Email without '@' separator is rejected
# ---------------------------------------------------------------------------

class TestEmailValidation:
    """ADSAT-9 AC-2: register_user must reject email addresses that lack '@'."""

    def test_email_without_at_sign_raises_value_error(self):
        """Scenario 2.1 — Email without '@' raises ValueError.

        Requirement: ADSAT-9 AC-2
        An email string that does not contain the '@' character must be
        rejected with the exact message 'Invalid email format'.
        """
        with pytest.raises(ValueError, match="Invalid email format"):
            register_user(username="valid_user", email="invalid-email-format")

    def test_valid_email_does_not_raise(self):
        """Scenario 2.2 — Valid email does NOT raise ValueError (no false positive).

        Requirement: ADSAT-9 AC-2
        An email string that contains '@' must not trigger the email
        validation error; the function must return a dict successfully.
        """
        result = register_user(username="valid_user", email="valid@example.com")
        assert isinstance(result, dict), (
            "register_user should return a dict for a valid email, not raise an exception."
        )


# ---------------------------------------------------------------------------
# Acceptance Criterion 3 — Whitespace trimming and default field initialisation
# ---------------------------------------------------------------------------

class TestWhitespaceTrimmingAndDefaults:
    """ADSAT-9 AC-3: register_user must trim whitespace and set default role/status."""

    def test_leading_trailing_whitespace_stripped_from_username(self):
        """Scenario 3.1a — Leading/trailing whitespace is stripped from username.

        Requirement: ADSAT-9 AC-3
        When username=' john_doe ' is supplied, the returned dict must store
        'john_doe' (no surrounding spaces).
        """
        result = register_user(username=" john_doe ", email="john@example.com ")
        assert result["username"] == "john_doe", (
            f"Expected username 'john_doe' after trimming, got '{result['username']}'"
        )

    def test_leading_trailing_whitespace_stripped_from_email(self):
        """Scenario 3.1b — Leading/trailing whitespace is stripped from email.

        Requirement: ADSAT-9 AC-3
        When email='john@example.com ' is supplied, the returned dict must
        store 'john@example.com' (no surrounding spaces).
        """
        result = register_user(username=" john_doe ", email="john@example.com ")
        assert result["email"] == "john@example.com", (
            f"Expected email 'john@example.com' after trimming, got '{result['email']}'"
        )

    def test_new_user_defaults_to_role_customer(self):
        """Scenario 3.2a — New user defaults to role 'customer'.

        Requirement: ADSAT-9 AC-3
        Every successfully registered user must have role='customer' in the
        returned dict, regardless of any whitespace in the inputs.
        """
        result = register_user(username=" john_doe ", email="john@example.com ")
        assert result["role"] == "customer", (
            f"Expected default role 'customer', got '{result['role']}'"
        )

    def test_new_user_defaults_to_status_active(self):
        """Scenario 3.2b — New user defaults to status 'active'.

        Requirement: ADSAT-9 AC-3
        Every successfully registered user must have status='active' in the
        returned dict, regardless of any whitespace in the inputs.
        """
        result = register_user(username=" john_doe ", email="john@example.com ")
        assert result["status"] == "active", (
            f"Expected default status 'active', got '{result['status']}'"
        )
