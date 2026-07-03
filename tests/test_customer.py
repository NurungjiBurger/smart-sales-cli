import unittest
from unittest.mock import patch
from customer import get_next_id, list_all, detail, search, update, delete


class TestCustomer(unittest.TestCase):

    @patch("customer.load_data")
    def test_get_next_id_empty(self, mock_load_data):
        mock_load_data.return_value = []
        self.assertEqual(get_next_id(), "C001")

    @patch("customer.load_data")
    def test_get_next_id_existing(self, mock_load_data):
        mock_load_data.return_value = [
            {"customer_id": "C001"},
            {"customer_id": "C005"},
        ]
        self.assertEqual(get_next_id(), "C006")

    @patch("customer.load_data")
    def test_get_next_id_with_non_standard_ids(self, mock_load_data):
        mock_load_data.return_value = [
            {"customer_id": "C001"},
            {"customer_id": "invalid"},
        ]
        self.assertEqual(get_next_id(), "C002")

    @patch("customer.load_data")
    def test_list_all_empty(self, mock_load_data):
        mock_load_data.return_value = []
        with patch("builtins.print") as mock_print:
            list_all()
            mock_print.assert_any_call("\n등록된 고객사가 없습니다.")

    @patch("customer.load_data")
    def test_list_all_with_data(self, mock_load_data):
        mock_load_data.return_value = [
            {"customer_id": "C001", "customer_name": "테스트", "manager_name": "홍길동", "email": "test@test.com"}
        ]
        with patch("builtins.print") as mock_print:
            list_all()
            mock_print.assert_any_call(f"{'C001':<8} {'테스트':<20} {'홍길동':<12} {'test@test.com':<30}")

    @patch("customer.load_data")
    def test_detail_found(self, mock_load_data):
        mock_load_data.return_value = [
            {"customer_id": "C001", "customer_name": "테스트", "manager_name": "홍길동", "email": "test@test.com"}
        ]
        with patch("builtins.print") as mock_print:
            detail("C001")
            mock_print.assert_any_call("고객사 ID: C001")
            mock_print.assert_any_call("고객사명: 테스트")

    @patch("customer.load_data")
    def test_detail_not_found(self, mock_load_data):
        mock_load_data.return_value = []
        with patch("builtins.print") as mock_print:
            detail("C999")
            mock_print.assert_any_call("고객사 C999를 찾을 수 없습니다.")

    @patch("customer.load_data")
    def test_search_found(self, mock_load_data):
        mock_load_data.return_value = [
            {"customer_id": "C001", "customer_name": "테스트", "manager_name": "홍길동", "email": "test@test.com"}
        ]
        with patch("builtins.print") as mock_print:
            search("테스트")
            mock_print.assert_any_call("\n--- '테스트' 검색 결과 ---")

    @patch("customer.load_data")
    def test_search_not_found(self, mock_load_data):
        mock_load_data.return_value = []
        with patch("builtins.print") as mock_print:
            search("없음")
            mock_print.assert_any_call("'없음' 검색 결과가 없습니다.")

    @patch("customer.load_data")
    @patch("customer.save_data")
    @patch("builtins.input")
    def test_update_found(self, mock_input, mock_save_data, mock_load_data):
        mock_load_data.return_value = [
            {"customer_id": "C001", "customer_name": "테스트", "manager_name": "홍길동", "email": "test@test.com"}
        ]
        # update: Enter for name, "새담당자" for manager, Enter for email
        mock_input.side_effect = ["", "새담당자", ""]
        update("C001")
        mock_save_data.assert_called_once()
        saved = mock_save_data.call_args[0][1]
        self.assertEqual(saved[0]["manager_name"], "새담당자")
        self.assertEqual(saved[0]["customer_name"], "테스트")  # unchanged
        self.assertEqual(saved[0]["email"], "test@test.com")  # unchanged

    @patch("customer.load_data")
    def test_update_not_found(self, mock_load_data):
        mock_load_data.return_value = []
        with patch("builtins.print") as mock_print:
            update("C999")
            mock_print.assert_any_call("고객사 C999를 찾을 수 없습니다.")

    @patch("customer.load_data")
    @patch("customer.save_data")
    @patch("builtins.input")
    def test_delete_confirmed(self, mock_input, mock_save_data, mock_load_data):
        mock_load_data.return_value = [
            {"customer_id": "C001", "customer_name": "테스트", "manager_name": "홍길동", "email": "test@test.com"}
        ]
        mock_input.return_value = "y"
        delete("C001")
        mock_save_data.assert_called_once()
        saved = mock_save_data.call_args[0][1]
        self.assertEqual(len(saved), 0)

    @patch("customer.load_data")
    @patch("customer.save_data")
    @patch("builtins.input")
    def test_delete_cancelled(self, mock_input, mock_save_data, mock_load_data):
        mock_load_data.return_value = [
            {"customer_id": "C001", "customer_name": "테스트", "manager_name": "홍길동", "email": "test@test.com"}
        ]
        mock_input.return_value = "n"
        delete("C001")
        mock_save_data.assert_not_called()

    @patch("customer.load_data")
    def test_delete_not_found(self, mock_load_data):
        mock_load_data.return_value = []
        with patch("builtins.print") as mock_print:
            delete("C999")
            mock_print.assert_any_call("고객사 C999를 찾을 수 없습니다.")


if __name__ == "__main__":
    unittest.main()