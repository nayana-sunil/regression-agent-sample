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

def calculate_discount(order_total: float, user_tier: str) -> float:
    if order_total < 0:
        raise ValueError('Order total cannot be negative')
    tier = user_tier.upper() if user_tier else 'REGULAR'
    if tier == 'VIP':
        discount = 0.20
    elif tier == 'REGULAR':
        discount = 0.05
    else:
        discount = 0.0
    return round(order_total * (1 - discount), 2)
