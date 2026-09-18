# Requirement Specification: Tiered Discounts (REG-200)

## 1. Membership Discounts (REG-202)
- **VIP Tier**: Grants 20% discount on final order total.
- **REGULAR Tier**: Grants 5% discount on final order total.
- **Unrecognized Tier**: Default to 0% discount.
- **Validation**: Negative order totals must throw a ValueError.
