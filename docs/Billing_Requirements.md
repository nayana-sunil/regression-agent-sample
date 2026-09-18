# Requirement Specification: Tiered Discounts (REG-200)

## 1. Membership Discounts & Rounding (REG-202)
- **VIP Tier**: Grants 20% discount on final order total.
- **REGULAR Tier**: Grants 5% discount on final order total.
- **Unrecognized Tier**: Default to 0% discount.
- **Percentage Discount Function**: Supports arbitrary percentage rates (e.g., 15%, 33%).
- **Rounding Logic**: Discount amounts and payable totals must be rounded to the nearest cent (ound(val, 2)), NOT truncated down.
  - Example: A .00 order with 15% off produces a .50 discount amount (.50 payable).
  - Example: A .99 order at 33% off produces a .30 discount amount (.69 payable).
- **Validation**: Order total less than 0.00 must raise a ValueError('Order total cannot be negative').
