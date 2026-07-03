import unittest
from unittest.mock import patch
from report import get_next_id, update, submit, approve, reject, withdraw, summary_by_customer


class TestReport(unittest.TestCase):

    @patch("report.load_data")
    def test_get_next_id_empty(self, mock_load_data):
        mock_load_data.return_value = []
        self.assertEqual(get_next_id(), "R001")

    @patch("report.load_data")
    def test_get_next_id_existing(self, mock_load_data):
        mock_load_data.return_value = [
            {"report_id": "R001"},
            {"report_id": "R005"},
        ]
        self.assertEqual(get_next_id(), "R006")

    @patch("report.load_data")
    def test_get_next_id_with_non_standard_ids(self, mock_load_data):
        mock_load_data.return_value = [
            {"report_id": "R001"},
            {"report_id": "invalid"},
        ]
        self.assertEqual(get_next_id(), "R002")

    @patch("report.load_data")
    @patch("report.save_data")
    @patch("builtins.input")
    def test_update_draft_ok(self, mock_input, mock_save_data, mock_load_data):
        mock_load_data.return_value = [
            {"report_id": "R001", "customer_id": "C001", "activity_date": "2026-06-09",
             "content": "old content", "status": "DRAFT"}
        ]
        mock_input.return_value = "new content"
        update("R001")
        mock_save_data.assert_called_once()
        saved = mock_save_data.call_args[0][1]
        self.assertEqual(saved[0]["content"], "new content")

    @patch("report.load_data")
    def test_update_non_draft_fails(self, mock_load_data):
        for status in ["SUBMITTED", "APPROVED", "REJECTED"]:
            mock_load_data.return_value = [
                {"report_id": "R001", "customer_id": "C001", "activity_date": "2026-06-09",
                 "content": "test", "status": status}
            ]
            with patch("builtins.print") as mock_print:
                update("R001")
                mock_print.assert_any_call(
                    f"영업일지 R001는 DRAFT 상태가 아니므로 수정할 수 없습니다. (현재: {status})"
                )

    @patch("report.load_data")
    def test_update_not_found(self, mock_load_data):
        mock_load_data.return_value = []
        with patch("builtins.print") as mock_print:
            update("R999")
            mock_print.assert_any_call("영업일지 R999를 찾을 수 없습니다.")

    # --- Status transitions ---

    @patch("report.load_data")
    @patch("report.save_data")
    def test_submit_draft_to_submitted(self, mock_save_data, mock_load_data):
        mock_load_data.return_value = [
            {"report_id": "R001", "status": "DRAFT"}
        ]
        submit("R001")
        mock_save_data.assert_called_once()
        saved = mock_save_data.call_args[0][1]
        self.assertEqual(saved[0]["status"], "SUBMITTED")

    @patch("report.load_data")
    def test_submit_non_draft_fails(self, mock_load_data):
        for status in ["SUBMITTED", "APPROVED", "REJECTED"]:
            mock_load_data.return_value = [
                {"report_id": "R001", "status": status}
            ]
            with patch("builtins.print") as mock_print:
                submit("R001")
                mock_print.assert_any_call(
                    f"영업일지 R001는 DRAFT 상태가 아닙니다. (현재: {status})"
                )

    @patch("report.load_data")
    def test_submit_not_found(self, mock_load_data):
        mock_load_data.return_value = []
        with patch("builtins.print") as mock_print:
            submit("R999")
            mock_print.assert_any_call("영업일지 R999를 찾을 수 없습니다.")

    @patch("report.load_data")
    @patch("report.save_data")
    def test_approve_submitted_to_approved(self, mock_save_data, mock_load_data):
        mock_load_data.return_value = [
            {"report_id": "R001", "status": "SUBMITTED"}
        ]
        approve("R001")
        mock_save_data.assert_called_once()
        saved = mock_save_data.call_args[0][1]
        self.assertEqual(saved[0]["status"], "APPROVED")

    @patch("report.load_data")
    def test_approve_non_submitted_fails(self, mock_load_data):
        for status in ["DRAFT", "APPROVED", "REJECTED"]:
            mock_load_data.return_value = [
                {"report_id": "R001", "status": status}
            ]
            with patch("builtins.print") as mock_print:
                approve("R001")
                mock_print.assert_any_call(
                    f"영업일지 R001는 SUBMITTED 상태가 아닙니다. (현재: {status})"
                )

    @patch("report.load_data")
    @patch("report.save_data")
    def test_reject_submitted_to_rejected(self, mock_save_data, mock_load_data):
        mock_load_data.return_value = [
            {"report_id": "R001", "status": "SUBMITTED"}
        ]
        reject("R001")
        mock_save_data.assert_called_once()
        saved = mock_save_data.call_args[0][1]
        self.assertEqual(saved[0]["status"], "REJECTED")

    @patch("report.load_data")
    def test_reject_non_submitted_fails(self, mock_load_data):
        for status in ["DRAFT", "APPROVED", "REJECTED"]:
            mock_load_data.return_value = [
                {"report_id": "R001", "status": status}
            ]
            with patch("builtins.print") as mock_print:
                reject("R001")
                mock_print.assert_any_call(
                    f"영업일지 R001는 SUBMITTED 상태가 아닙니다. (현재: {status})"
                )

    @patch("report.load_data")
    @patch("report.save_data")
    def test_withdraw_submitted_to_draft(self, mock_save_data, mock_load_data):
        mock_load_data.return_value = [
            {"report_id": "R001", "status": "SUBMITTED"}
        ]
        withdraw("R001")
        mock_save_data.assert_called_once()
        saved = mock_save_data.call_args[0][1]
        self.assertEqual(saved[0]["status"], "DRAFT")

    @patch("report.load_data")
    def test_withdraw_non_submitted_fails(self, mock_load_data):
        for status in ["DRAFT", "APPROVED", "REJECTED"]:
            mock_load_data.return_value = [
                {"report_id": "R001", "status": status}
            ]
            with patch("builtins.print") as mock_print:
                withdraw("R001")
                mock_print.assert_any_call(
                    f"영업일지 R001는 SUBMITTED 상태가 아닙니다. (현재: {status})"
                )

    # --- Summary ---

    @patch("report.load_data")
    def test_summary_empty(self, mock_load_data):
        mock_load_data.side_effect = [[], []]  # reports empty, customers empty
        with patch("builtins.print") as mock_print:
            summary_by_customer()
            mock_print.assert_any_call("\n등록된 영업일지가 없습니다.")

    @patch("report.load_data")
    def test_summary_with_data(self, mock_load_data):
        mock_load_data.side_effect = [
            [  # reports
                {"customer_id": "C001", "status": "APPROVED"},
                {"customer_id": "C001", "status": "DRAFT"},
                {"customer_id": "C002", "status": "SUBMITTED"},
            ],
            [  # customers
                {"customer_id": "C001", "customer_name": "고객사A"},
                {"customer_id": "C002", "customer_name": "고객사B"},
            ],
        ]
        with patch("builtins.print") as mock_print:
            summary_by_customer()
            # C001 line
            mock_print.assert_any_call(f"{'C001':<12} {'고객사A':<20} {'2':<6} {'1':<8} {'0':<12} {'1':<10} {'0':<10}")
            # C002 line
            mock_print.assert_any_call(f"{'C002':<12} {'고객사B':<20} {'1':<6} {'0':<8} {'1':<12} {'0':<10} {'0':<10}")


if __name__ == "__main__":
    unittest.main()