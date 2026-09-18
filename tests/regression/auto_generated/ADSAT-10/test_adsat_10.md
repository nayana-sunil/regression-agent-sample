# Regression Scenarios — ADSAT-10: Tiered Discount Calculation & Rounding Logic

**Ticket:** ADSAT-10  
**PRD Section:** REG-200 / REG-202 (docs/Billing_Requirements.md)  
**Functions under test:** `calculate_discount_amount`, `calculate_discount` (src/user_service.py)

---

## Scenario 1 — Rounding: 15% discount on a terminating decimal total
**Requirement:** ADSAT-10 AC1; REG-202 Rounding Logic  
**Preconditions:** None  
**Steps:**
1. Call `calculate_discount_amount(order_total=10.00, discount_percent=15.0)`.

**Expected result:** Returns `1.50` (rounded to nearest cent). Must NOT return `1.00` (truncated).

---

## Scenario 2 — Rounding: 33% discount on a non-terminating decimal total
**Requirement:** ADSAT-10 AC1; REG-202 Rounding Logic (non-terminating example)  
**Preconditions:** None  
**Steps:**
1. Call `calculate_discount_amount(order_total=9.99, discount_percent=33.0)`.

**Expected result:** Returns `3.30` (rounded to nearest cent, not truncated to `3.29`).

---

## Scenario 3 — VIP tier: 20% discount applied to $100.00 order
**Requirement:** ADSAT-10 AC2; REG-202 VIP Tier  
**Preconditions:** User tier is `'VIP'`.  
**Steps:**
1. Call `calculate_discount(order_total=100.00, user_tier='VIP')`.

**Expected result:** Returns `80.00` (final payable after 20% discount).

---

## Scenario 4 — REGULAR tier: 5% discount applied to $100.00 order
**Requirement:** ADSAT-10 AC3; REG-202 REGULAR Tier  
**Preconditions:** User tier is `'REGULAR'`.  
**Steps:**
1. Call `calculate_discount(order_total=100.00, user_tier='REGULAR')`.

**Expected result:** Returns `95.00` (final payable after 5% discount).

---

## Scenario 5 — Negative order total rejected by `calculate_discount`
**Requirement:** ADSAT-10 AC4; REG-202 Validation  
**Preconditions:** None  
**Steps:**
1. Call `calculate_discount(order_total=-50.00, user_tier='VIP')`.

**Expected result:** Raises `ValueError` with message `"Order total cannot be negative"`.

---

## Scenario 6 — Negative order total rejected by `calculate_discount_amount`
**Requirement:** ADSAT-10 AC4; REG-202 Validation  
**Preconditions:** None  
**Steps:**
1. Call `calculate_discount_amount(order_total=-50.00, discount_percent=15.0)`.

**Expected result:** Raises `ValueError` with message `"Order total cannot be negative"`.

---

## Scenario 7 — Unrecognized tier defaults to 0% discount
**Requirement:** REG-202 Unrecognized Tier  
**Preconditions:** User tier is an unrecognized string (e.g. `'GOLD'`).  
**Steps:**
1. Call `calculate_discount(order_total=100.00, user_tier='GOLD')`.

**Expected result:** Returns `100.00` (no discount applied — 0% for unrecognized tier).

---

## Scenario 8 — Rounding of payable total: REGULAR tier on non-terminating total
**Requirement:** REG-202 Rounding Logic (payable total must also be rounded)  
**Preconditions:** User tier is `'REGULAR'`.  
**Steps:**
1. Call `calculate_discount(order_total=9.99, user_tier='REGULAR')`.

**Expected result:** Returns `9.49` (5% of $9.99 = $0.4995, discount rounded to $0.50; payable = $9.49).

---

## Scenario 9 — Rounding of payable total: VIP tier on non-terminating total
**Requirement:** REG-202 Rounding Logic (payable total must also be rounded); REG-202 VIP Tier  
**Preconditions:** User tier is `'VIP'`.  
**Steps:**
1. Call `calculate_discount(order_total=9.99, user_tier='VIP')`.

**Expected result:** Returns `7.99` (20% of $9.99 = $1.998, discount rounded to $2.00; payable = $7.99).
