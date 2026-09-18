# Requirement Specification: User Management (REG-100)

## 1. User Registration (REG-101)
- **Validation**:
  - username must be a non-empty string.
  - email must contain a valid '@' domain separator.
- **Default State**:
  - Newly created users are assigned ole = 'customer' and status = 'active'.

## 2. Edge Cases
- Whitespace-only usernames should be rejected.
