import unittest
from unittest.mock import patch
import os
import csv
import tempfile
from exporter import export_customers_csv, EXPORT_DIR


class TestExporter(unittest.TestCase):

    def setUp(self):
        # 테스트 시작 전 exports 디렉터리 정리
        if os.path.exists(EXPORT_DIR):
            for f in os.listdir(EXPORT_DIR):
                os.remove(os.path.join(EXPORT_DIR, f))

    @patch("exporter.load_data")
    def test_export_empty(self, mock_load_data):
        mock_load_data.return_value = []
        with patch("builtins.print") as mock_print:
            export_customers_csv()
            mock_print.assert_any_call("내보낼 고객사 데이터가 없습니다.")

    @patch("exporter.load_data")
    def test_export_with_data(self, mock_load_data):
        mock_load_data.return_value = [
            {"customer_id": "C001", "customer_name": "테스트", "manager_name": "홍길동", "email": "test@test.com"}
        ]
        export_customers_csv()

        # exports 디렉터리가 생성되었는지 확인
        self.assertTrue(os.path.exists(EXPORT_DIR))

        # CSV 파일이 생성되었는지 확인
        files = os.listdir(EXPORT_DIR)
        csv_files = [f for f in files if f.startswith("customers_export_") and f.endswith(".csv")]
        self.assertEqual(len(csv_files), 1)

        # CSV 내용 검증
        filepath = os.path.join(EXPORT_DIR, csv_files[0])
        with open(filepath, "r", encoding="utf-8-sig", newline="") as f:
            reader = csv.DictReader(f)
            rows = list(reader)
            self.assertEqual(len(rows), 1)
            self.assertEqual(rows[0]["customer_id"], "C001")
            self.assertEqual(rows[0]["customer_name"], "테스트")
            self.assertEqual(rows[0]["manager_name"], "홍길동")
            self.assertEqual(rows[0]["email"], "test@test.com")

    @patch("exporter.load_data")
    def test_export_multiple_customers(self, mock_load_data):
        mock_load_data.return_value = [
            {"customer_id": "C001", "customer_name": "고객사A", "manager_name": "김철수", "email": "a@test.com"},
            {"customer_id": "C002", "customer_name": "고객사B", "manager_name": "이영희", "email": "b@test.com"},
        ]
        export_customers_csv()

        files = os.listdir(EXPORT_DIR)
        csv_files = [f for f in files if f.startswith("customers_export_") and f.endswith(".csv")]
        filepath = os.path.join(EXPORT_DIR, csv_files[0])

        with open(filepath, "r", encoding="utf-8-sig", newline="") as f:
            reader = csv.DictReader(f)
            rows = list(reader)
            self.assertEqual(len(rows), 2)
            self.assertEqual(rows[0]["customer_id"], "C001")
            self.assertEqual(rows[1]["customer_id"], "C002")

    def tearDown(self):
        # 테스트 후 exports 디렉터리 정리
        if os.path.exists(EXPORT_DIR):
            for f in os.listdir(EXPORT_DIR):
                os.remove(os.path.join(EXPORT_DIR, f))


if __name__ == "__main__":
    unittest.main()