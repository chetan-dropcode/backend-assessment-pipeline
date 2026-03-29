import json
import random
from datetime import datetime, timedelta

customers = []
for i in range(1, 25):
    customers.append({
        "customer_id": f"CUST-{i:04d}",
        "first_name": f"User{i}",
        "last_name": "Test",
        "email": f"user{i}@example.com",
        "phone": f"+919876543{i:03d}",
        "address": f"{i} Main St, Mumbai",
        "date_of_birth": (datetime.now() - timedelta(days=random.randint(7000, 15000))).strftime("%Y-%m-%d"),
        "account_balance": round(random.uniform(100.0, 50000.0), 2),
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })

with open('mock-server/data/customers.json', 'w') as f:
    json.dump(customers, f, indent=4)
    
print("customers.json created successfully!")