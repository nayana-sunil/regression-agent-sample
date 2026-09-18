"""
Regression Scenarios — ADSAT-9: User Registration Validation & Role Defaults
================================================================================
This file is the human-readable scenario specification for ADSAT-9.
It is NOT a runnable test file; see test_adsat_9.py for the pytest implementation.

Requirement source
------------------
Jira ticket ADSAT-9 — User Registration Validation & Role Defaults

Acceptance Criteria covered
---------------------------
AC-1  register_user must raise ValueError("Username cannot be empty") when the
      username is blank or whitespace-only.
AC-2  register_user must raise ValueError("Invalid email format") when the email
      string does not contain '@'.
AC-3  For valid inputs, register_user must strip leading/trailing whitespace from
      username AND email, and set role='customer' and status='active'.

Scenarios
---------

ADSAT-9-TC-01 — Whitespace-only username is rejected  [AC-1 | Negative]
  Preconditions : register_user is importable from src.user_service.
  Steps         : Call register_user(username="   ", email="test@example.com").
  Expected      : ValueError raised with message "Username cannot be empty".

ADSAT-9-TC-02 — Empty-string username is rejected  [AC-1 | Negative / Edge]
  Preconditions : register_user is importable from src.user_service.
  Steps         : Call register_user(username="", email="test@example.com").
  Expected      : ValueError raised with message "Username cannot be empty".

ADSAT-9-TC-03 — Email without '@' is rejected  [AC-2 | Negative]
  Preconditions : register_user is importable from src.user_service.
  Steps         : Call register_user(username="valid_user", email="invalid-email-format").
  Expected      : ValueError raised with message "Invalid email format".

ADSAT-9-TC-04 — Empty-string email is rejected  [AC-2 | Negative / Edge]
  Preconditions : register_user is importable from src.user_service.
  Steps         : Call register_user(username="valid_user", email="").
  Expected      : ValueError raised with message "Invalid email format".

ADSAT-9-TC-05 — Valid inputs with surrounding whitespace are trimmed; defaults set  [AC-3 | Positive]
  Preconditions : register_user is importable from src.user_service.
  Steps         : Call register_user(username=" john_doe ", email="john@example.com ").
  Expected      : Returned dict has username="john_doe", email="john@example.com",
                  role="customer", status="active".

ADSAT-9-TC-06 — Valid inputs without whitespace also produce correct defaults  [AC-3 | Positive / Baseline]
  Preconditions : register_user is importable from src.user_service.
  Steps         : Call register_user(username="jane_doe", email="jane@example.com").
  Expected      : Returned dict has username="jane_doe", email="jane@example.com",
                  role="customer", status="active".
"""
