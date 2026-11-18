"""
Script to create sample Excel and CSV files for user upload testing
"""
import pandas as pd
from datetime import datetime

data = [
    {"order_id": "ORD-UPLOAD-001", "store_id": "STORE_01", "customer_name": "Lê Văn Tám", "customer_phone": "0981112233", "order_time": "2026-11-16 10:15:00", "status": "completed", "cancel_reason": None, "total_amount": 350000.0, "is_test": 0},
    {"order_id": "ORD-UPLOAD-002", "store_id": "STORE_04", "customer_name": "Ngô Thị Mai", "customer_phone": "0912223344", "order_time": "2026-11-16 17:30:00", "status": "cancelled", "cancel_reason": "out_of_stock_pos_delay", "total_amount": 540000.0, "is_test": 0},
    {"order_id": "ORD-UPLOAD-003", "store_id": "STORE_04", "customer_name": "Phan Quốc Bảo", "customer_phone": "0933334455", "order_time": "2026-11-16 18:10:00", "status": "cancelled", "cancel_reason": "out_of_stock_pos_delay", "total_amount": 220000.0, "is_test": 0},
    {"order_id": "ORD-UPLOAD-004", "store_id": "STORE_02", "customer_name": "Vũ Thu Trang", "customer_phone": "0944445566", "order_time": "2026-11-16 14:00:00", "status": "completed", "cancel_reason": None, "total_amount": 180000.0, "is_test": 0},
    {"order_id": "TEST-UPLOAD-999", "store_id": "STORE_04", "customer_name": "Test Account", "customer_phone": "0900000000", "order_time": "2026-11-16 11:00:00", "status": "cancelled", "cancel_reason": "test_script", "total_amount": 0.0, "is_test": 1},
]

df = pd.DataFrame(data)
df.to_excel("sample_orders.xlsx", index=False)
df.to_csv("sample_orders.csv", index=False, encoding="utf-8-sig")
print("Generated sample_orders.xlsx and sample_orders.csv successfully.")
