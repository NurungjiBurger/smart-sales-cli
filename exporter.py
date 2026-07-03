import os
import csv
from datetime import datetime
from storageai import load_data

EXPORT_DIR = "exports"
FILE_PREFIX = "customers_export"


def export_customers_csv():
    """고객사 목록을 CSV 파일로 내보낸다. (exports/ 폴더에 저장)"""
    customers = load_data("customers")
    if not customers:
        print("내보낼 고객사 데이터가 없습니다.")
        return

    os.makedirs(EXPORT_DIR, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{FILE_PREFIX}_{timestamp}.csv"
    filepath = os.path.join(EXPORT_DIR, filename)

    with open(filepath, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["customer_id", "customer_name", "manager_name", "email"])
        writer.writeheader()
        for c in customers:
            writer.writerow({
                "customer_id": c["customer_id"],
                "customer_name": c["customer_name"],
                "manager_name": c["manager_name"],
                "email": c["email"],
            })

    print(f"CSV 내보내기 완료: {filepath} ({len(customers)}건)")