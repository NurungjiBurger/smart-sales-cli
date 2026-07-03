import re
from datetime import datetime


def validate_required(value, field_name):
    """필수 입력값 검증. 빈 문자열이면 오류 메시지를 반환한다."""
    if not value or not value.strip():
        return f"{field_name}은(는) 필수 입력입니다."
    return None


def validate_customer_id(customer_id):
    """고객사 ID 형식 검증 (C + 숫자 3자리)"""
    if not re.match(r"^C\d{3}$", customer_id):
        return "고객사 ID는 'C' 뒤에 숫자 3자리 형식이어야 합니다. (예: C001)"
    return None


def validate_date(date_str):
    """날짜 형식 및 실제 존재하는 날짜 검증 (YYYY-MM-DD)"""
    if not re.match(r"^\d{4}-\d{2}-\d{2}$", date_str):
        return "날짜는 YYYY-MM-DD 형식이어야 합니다. (예: 2026-06-09)"
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        return "존재하지 않는 날짜입니다."
    return None