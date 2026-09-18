"""Regression tests for ADSAT-10: Tiered Discount Calculation & Rounding Logic.

Requirements covered:
  - ADSAT-10 Acceptance Criteria (AC1–AC4)
  - REG-200 / REG-202: Membership Discounts & Rounding (docs/Billing_Requirements.md)

Functions under test:
  - src.user_service.calculate_discount_amount
  - src.user_service.calculate_discount
"""

import pytest
from src.user_service import calculate_discount_amount, calculate_discount


# ---------------------------------------------------------------------------
# Scenario 1 — Rounding: 15% discount on a terminating decimal total
# Requirement: ADSAT-10 AC1; REG-202 Rounding Logic
# ---------------------------------------------------------------------------
class TestCalculateDiscountAmountRounding:
    def test_15_percent_on_10_dollars_rounds_to_nearest_cent(self):
        """$10.00 × 15% = $1.50 (rounded), not $1.00 (truncated). ADSAT-10 AC1."""
        result = calculate_discount_amount(10.00, 15.0)
        assert result == 1.50, (
            f"Expected discount amount 1.50 but got {result}. "
            "Discount must be rounded to nearest cent, not truncated."
        )

    # Scenario 2 — Rounding: 33% discount on a non-terminating decimal total
    # Requirement: ADSAT-10 AC1; REG-202 Rounding Logic (non-terminating example)
    def test_33_percent_on_9_99_rounds_to_nearest_cent(self):
        """$9.99 × 33% = $3.2967 → rounded to $3.30. ADSAT-10 AC1 (non-terminating case)."""
        result = calculate_discount_amount(9.99, 33.0)
        assert result == 3.30, (
            f"Expected discount amount 3.30 but got {result}. "
            "Non-terminating discount must be rounded, not truncated."
        )


# ---------------------------------------------------------------------------
# Scenario 3 — VIP tier: 20% discount applied to $100.00 order
# Requirement: ADSAT-10 AC2; REG-202 VIP Tier
# ---------------------------------------------------------------------------
class TestCalculateDiscountVIPTier:
    def test_vip_tier_100_dollars_returns_80_dollars(self):
        """VIP tier on $100.00 → 20% off → payable $80.00. ADSAT-10 AC2."""
        result = calculate_discount(100.00, 'VIP')
        assert result == 80.00, (
            f"Expected payable total 80.00 for VIP tier but got {result}."
        )

    def test_vip_tier_case_insensitive(self):
        """Tier matching must be case-insensitive per implementation contract. REG-202 VIP Tier."""
        result = calculate_discount(100.00, 'vip')
        assert result == 80.00, (
            f"Expected payable total 80.00 for lowercase 'vip' tier but got {result}."
        )

    # Scenario 9 — Rounding of payable total: VIP tier on non-terminating total
    # Requirement: REG-202 Rounding Logic; REG-202 VIP Tier
    def test_vip_tier_9_99_payable_total_is_rounded(self):
        """VIP tier on $9.99 → 20% off → discount $2.00 (rounded from $1.998) → payable $7.99. REG-202."""
        result = calculate_discount(9.99, 'VIP')
        assert result == 7.99, (
            f"Expected payable total 7.99 for VIP tier on $9.99 but got {result}. "
            "Payable total must be rounded to nearest cent."
        )


# ---------------------------------------------------------------------------
# Scenario 4 — REGULAR tier: 5% discount applied to $100.00 order
# Requirement: ADSAT-10 AC3; REG-202 REGULAR Tier
# ---------------------------------------------------------------------------
class TestCalculateDiscountRegularTier:
    def test_regular_tier_100_dollars_returns_95_dollars(self):
        """REGULAR tier on $100.00 → 5% off → payable $95.00. ADSAT-10 AC3."""
        result = calculate_discount(100.00, 'REGULAR')
        assert result == 95.00, (
            f"Expected payable total 95.00 for REGULAR tier but got {result}."
        )

    def test_regular_tier_case_insensitive(self):
        """Tier matching must be case-insensitive per implementation contract. REG-202 REGULAR Tier."""
        result = calculate_discount(100.00, 'regular')
        assert result == 95.00, (
            f"Expected payable total 95.00 for lowercase 'regular' tier but got {result}."
        )

    # Scenario 8 — Rounding of payable total: REGULAR tier on non-terminating total
    # Requirement: REG-202 Rounding Logic (payable total must also be rounded)
    def test_regular_tier_9_99_payable_total_is_rounded(self):
        """REGULAR tier on $9.99 → 5% off → discount $0.50 (rounded from $0.4995) → payable $9.49. REG-202."""
        result = calculate_discount(9.99, 'REGULAR')
        assert result == 9.49, (
            f"Expected payable total 9.49 for REGULAR tier on $9.99 but got {result}. "
            "Payable total must be rounded to nearest cent."
        )


# ---------------------------------------------------------------------------
# Scenario 5 — Negative order total rejected by calculate_discount
# Requirement: ADSAT-10 AC4; REG-202 Validation
# ---------------------------------------------------------------------------
class TestCalculateDiscountNegativeOrderTotal:
    def test_negative_order_total_raises_value_error(self):
        """calculate_discount with negative total must raise ValueError. ADSAT-10 AC4."""
        with pytest.raises(ValueError, match="Order total cannot be negative"):
            calculate_discount(-50.00, 'VIP')

    def test_negative_order_total_regular_tier_raises_value_error(self):
        """Negative total must be rejected regardless of tier. ADSAT-10 AC4; REG-202 Validation."""
        with pytest.raises(ValueError, match="Order total cannot be negative"):
            calculate_discount(-0.01, 'REGULAR')


# ---------------------------------------------------------------------------
# Scenario 6 — Negative order total rejected by calculate_discount_amount
# Requirement: ADSAT-10 AC4; REG-202 Validation
# ---------------------------------------------------------------------------
class TestCalculateDiscountAmountNegativeOrderTotal:
    def test_negative_order_total_raises_value_error(self):
        """calculate_discount_amount with negative total must raise ValueError. ADSAT-10 AC4."""
        with pytest.raises(ValueError, match="Order total cannot be negative"):
            calculate_discount_amount(-50.00, 15.0)

    def test_negative_order_total_zero_percent_raises_value_error(self):
        """Even a 0% discount rate must not bypass the negative-total guard. REG-202 Validation."""
        with pytest.raises(ValueError, match="Order total cannot be negative"):
            calculate_discount_amount(-1.00, 0.0)


# ---------------------------------------------------------------------------
# Scenario 7 — Unrecognized tier defaults to 0% discount
# Requirement: REG-202 Unrecognized Tier
# ---------------------------------------------------------------------------
class TestCalculateDiscountUnrecognizedTier:
    def test_unrecognized_tier_applies_zero_discount(self):
        """An unrecognized tier (e.g. 'GOLD') must default to 0% discount. REG-202."""
        result = calculate_discount(100.00, 'GOLD')
        assert result == 100.00, (
            f"Expected payable total 100.00 for unrecognized tier 'GOLD' but got {result}. "
            "Unrecognized tiers must default to 0% discount."
        )

    def test_empty_string_tier_applies_zero_discount_or_regular(self):
        """An empty-string tier falls back to REGULAR (5%) per implementation default. REG-202."""
        # Per implementation: user_tier falsy → defaults to 'REGULAR' → 5% discount
        result = calculate_discount(100.00, '')
        assert result == 95.00, (
            f"Expected payable total 95.00 when tier is empty string (defaults to REGULAR) but got {result}."
        )
