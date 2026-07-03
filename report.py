from storageai import load_data, save_data
from validator import validate_required, validate_date

DATA_FILE = "sales_reports"
CUSTOMER_FILE = "customers"


def get_next_id():
    """현재 최대 report_id 다음 값을 계산한다. (R001, R002, ...)"""
    reports = load_data(DATA_FILE)
    max_num = 0
    for r in reports:
        rid = r.get("report_id", "R000")
        if rid.startswith("R") and rid[1:].isdigit():
            num = int(rid[1:])
            if num > max_num:
                max_num = num
    return f"R{max_num + 1:03d}"


def _customer_exists(customer_id):
    """고객사 ID가 존재하는지 확인한다."""
    customers = load_data(CUSTOMER_FILE)
    return any(c["customer_id"] == customer_id for c in customers)


def _get_customer_name(customer_id):
    """고객사 ID로 고객사명을 조회한다."""
    customers = load_data(CUSTOMER_FILE)
    for c in customers:
        if c["customer_id"] == customer_id:
            return c["customer_name"]
    return "(알 수 없음)"


def register():
    """영업일지 등록"""
    print("\n--- 영업일지 등록 ---")
    report_id = get_next_id()
    print(f"영업일지 ID: {report_id}")

    customer_id = input("고객사 ID: ").strip()
    err = validate_required(customer_id, "고객사 ID")
    if err:
        print(err)
        return
    if not _customer_exists(customer_id):
        print(f"고객사 {customer_id}가 존재하지 않습니다.")
        return

    activity_date = input("활동일자 (YYYY-MM-DD): ").strip()
    err = validate_required(activity_date, "활동일자")
    if err:
        print(err)
        return
    err = validate_date(activity_date)
    if err:
        print(err)
        return

    content = input("활동 내용: ").strip()
    err = validate_required(content, "활동 내용")
    if err:
        print(err)
        return

    reports = load_data(DATA_FILE)
    reports.append({
        "report_id": report_id,
        "customer_id": customer_id,
        "activity_date": activity_date,
        "content": content,
        "status": "DRAFT",
    })
    save_data(DATA_FILE, reports)
    print(f"영업일지 {report_id} 등록 완료.")


def list_all():
    """전체 영업일지 목록 출력"""
    reports = load_data(DATA_FILE)
    if not reports:
        print("\n등록된 영업일지가 없습니다.")
        return
    print("\n--- 영업일지 목록 ---")
    print(f"{'ID':<8} {'고객사':<20} {'고객사명':<16} {'활동일자':<14} {'상태':<12} {'내용'}")
    print("-" * 90)
    for r in reports:
        cname = _get_customer_name(r["customer_id"])
        content_preview = r["content"][:30] + "..." if len(r["content"]) > 30 else r["content"]
        print(f"{r['report_id']:<8} {r['customer_id']:<20} {cname:<16} {r['activity_date']:<14} {r['status']:<12} {content_preview}")


def update(report_id):
    """영업일지 내용 수정 (DRAFT 상태만 가능)"""
    reports = load_data(DATA_FILE)
    for r in reports:
        if r["report_id"] == report_id:
            if r["status"] != "DRAFT":
                print(f"영업일지 {report_id}는 DRAFT 상태가 아니므로 수정할 수 없습니다. (현재: {r['status']})")
                return
            print(f"\n--- 영업일지 수정 ({report_id}) ---")
            print(f"현재 내용: {r['content']}")
            new_content = input("새 내용 (Enter 유지): ").strip()
            if new_content:
                r["content"] = new_content
            save_data(DATA_FILE, reports)
            print(f"영업일지 {report_id} 수정 완료.")
            return
    print(f"영업일지 {report_id}를 찾을 수 없습니다.")


def _transition_status(report_id, action, required_status, target_status, action_label):
    """상태 전이 공통 로직"""
    reports = load_data(DATA_FILE)
    for r in reports:
        if r["report_id"] == report_id:
            if r["status"] != required_status:
                print(f"영업일지 {report_id}는 {required_status} 상태가 아닙니다. (현재: {r['status']})")
                return
            r["status"] = target_status
            save_data(DATA_FILE, reports)
            print(f"영업일지 {report_id} {action_label} 완료. (상태: {required_status} → {target_status})")
            return
    print(f"영업일지 {report_id}를 찾을 수 없습니다.")


def submit(report_id):
    """영업일지 상신 (DRAFT → SUBMITTED)"""
    _transition_status(report_id, "submit", "DRAFT", "SUBMITTED", "상신")


def approve(report_id):
    """영업일지 승인 (SUBMITTED → APPROVED)"""
    _transition_status(report_id, "approve", "SUBMITTED", "APPROVED", "승인")


def reject(report_id):
    """영업일지 반려 (SUBMITTED → REJECTED)"""
    _transition_status(report_id, "reject", "SUBMITTED", "REJECTED", "반려")


def withdraw(report_id):
    """영업일지 회수 (SUBMITTED → DRAFT)"""
    _transition_status(report_id, "withdraw", "SUBMITTED", "DRAFT", "회수")


def summary_by_customer():
    """고객사별 활동 요약"""
    reports = load_data(DATA_FILE)
    customers = load_data(CUSTOMER_FILE)

    # 고객사명 매핑
    name_map = {c["customer_id"]: c["customer_name"] for c in customers}

    # 집계
    summary = {}
    for r in reports:
        cid = r["customer_id"]
        if cid not in summary:
            summary[cid] = {"total": 0, "DRAFT": 0, "SUBMITTED": 0, "APPROVED": 0, "REJECTED": 0}
        summary[cid]["total"] += 1
        summary[cid][r["status"]] += 1

    if not summary:
        print("\n등록된 영업일지가 없습니다.")
        return

    print("\n--- 고객사별 활동 요약 ---")
    print(f"{'고객사 ID':<12} {'고객사명':<20} {'전체':<6} {'DRAFT':<8} {'SUBMITTED':<12} {'APPROVED':<10} {'REJECTED':<10}")
    print("-" * 78)
    for cid in sorted(summary):
        cname = name_map.get(cid, "(알 수 없음)")
        s = summary[cid]
        print(f"{cid:<12} {cname:<20} {s['total']:<6} {s['DRAFT']:<8} {s['SUBMITTED']:<12} {s['APPROVED']:<10} {s['REJECTED']:<10}")
