def register_user(username: str, email: str) -> dict:
    if not username or not username.strip():
        raise ValueError('Username cannot be empty')
    if not email or '@' not in email:
        raise ValueError('Invalid email format')
    return {
        'id': 'USR-9999',
        'username': username.strip(),
        'email': email.strip(),
        'role': 'customer',
        'status': 'active'
    }

def calculate_discount_amount(order_total: float, discount_percent: float) -> float:
    if order_total < 0:
        raise ValueError('Order total cannot be negative')
    return round(order_total * (discount_percent / 100.0), 2)

def calculate_discount(order_total: float, user_tier: str) -> float:
    if order_total < 0:
        raise ValueError('Order total cannot be negative')
    tier = user_tier.upper() if user_tier else 'REGULAR'
    if tier == 'VIP':
        discount_pct = 20.0
    elif tier == 'REGULAR':
        discount_pct = 5.0
    else:
        discount_pct = 0.0
    
    discount_amt = calculate_discount_amount(order_total, discount_pct)
    return round(order_total - discount_amt, 2)
