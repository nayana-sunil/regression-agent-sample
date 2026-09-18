# Regression Scenarios — ADSAT-9: User Registration Validation & Role Defaults

## Ticket Summary
When registering a new user, `register_user()` must (1) reject blank/whitespace-only usernames, (2) reject email addresses that lack the `@` separator, and (3) trim whitespace from valid inputs and initialise every new account with `role = 'customer'` and `status = 'active'`.

---

## Acceptance Criterion 1 — Blank / whitespace-only username is rejected
> *Given a username consisting of empty spaces or blank input, `register_user` must throw `ValueError("Username cannot be empty")`.*

### Scenario 1.1 — Whitespace-only username raises ValueError (positive error path)
- **Preconditions:** `register_user` is importable from `src.user_service`.
- **Steps:**
  1. Call `register_user(username="   ", email="test@example.com")`.
- **Expected result:** `ValueError` is raised with the message `"Username cannot be empty"`.
- **Requirement:** ADSAT-9 AC-1

### Scenario 1.2 — Empty-string username raises ValueError (edge case: zero-length string)
- **Preconditions:** `register_user` is importable from `src.user_service`.
- **Steps:**
  1. Call `register_user(username="", email="test@example.com")`.
- **Expected result:** `ValueError` is raised with the message `"Username cannot be empty"`.
- **Requirement:** ADSAT-9 AC-1

### Scenario 1.3 — Valid username does NOT raise ValueError (negative: no false positive)
- **Preconditions:** `register_user` is importable from `src.user_service`.
- **Steps:**
  1. Call `register_user(username="valid_user", email="valid@example.com")`.
- **Expected result:** No exception is raised; a dict is returned.
- **Requirement:** ADSAT-9 AC-1

---

## Acceptance Criterion 2 — Email without `@` separator is rejected
> *Given an email string lacking the `@` separator, `register_user` must throw `ValueError("Invalid email format")`.*

### Scenario 2.1 — Email without `@` raises ValueError (positive error path)
- **Preconditions:** `register_user` is importable from `src.user_service`.
- **Steps:**
  1. Call `register_user(username="valid_user", email="invalid-email-format")`.
- **Expected result:** `ValueError` is raised with the message `"Invalid email format"`.
- **Requirement:** ADSAT-9 AC-2

### Scenario 2.2 — Valid email does NOT raise ValueError (negative: no false positive)
- **Preconditions:** `register_user` is importable from `src.user_service`.
- **Steps:**
  1. Call `register_user(username="valid_user", email="valid@example.com")`.
- **Expected result:** No exception is raised; a dict is returned.
- **Requirement:** ADSAT-9 AC-2

---

## Acceptance Criterion 3 — Whitespace trimming and default field initialisation
> *Given valid inputs with surrounding whitespace (e.g. `username=" john_doe "`, `email="john@example.com "`), the function must trim whitespace and assign `role = 'customer'` and `status = 'active'`.*

### Scenario 3.1 — Leading/trailing whitespace is stripped from username and email (positive)
- **Preconditions:** `register_user` is importable from `src.user_service`.
- **Steps:**
  1. Call `register_user(username=" john_doe ", email="john@example.com ")`.
- **Expected result:**
  - Returned dict key `username` equals `"john_doe"` (no surrounding spaces).
  - Returned dict key `email` equals `"john@example.com"` (no surrounding spaces).
- **Requirement:** ADSAT-9 AC-3

### Scenario 3.2 — New user defaults to role `'customer'` and status `'active'` (positive)
- **Preconditions:** `register_user` is importable from `src.user_service`.
- **Steps:**
  1. Call `register_user(username=" john_doe ", email="john@example.com ")`.
- **Expected result:**
  - Returned dict key `role` equals `"customer"`.
  - Returned dict key `status` equals `"active"`.
- **Requirement:** ADSAT-9 AC-3
