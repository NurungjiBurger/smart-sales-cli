from storageai import load_data, save_data
from validator import validate_required

DATA_FILE = "customers"


def get_next_id():
    """현재 최대 customer_id 다음 값을 계산한다. (C001, C002, ...)"""
    customers = load_data(DATA_FILE)
    max_num = 0
    for c in customers:
        cid = c.get("customer_id", "C000")
        if cid.startswith("C") and cid[1:].isdigit():
            num = int(cid[1:])
            if num > max_num:
                max_num = num
    return f"C{max_num + 1:03d}"


def register():
    """고객사 등록"""
    print("\n--- 고객사 등록 ---")
    customer_id = get_next_id()
    print(f"고객사 ID: {customer_id}")

    customer_name = input("고객사명: ").strip()
    err = validate_required(customer_name, "고객사명")
    if err:
        print(err)
        return

    manager_name = input("담당자명: ").strip()
    err = validate_required(manager_name, "담당자명")
    if err:
        print(err)
        return

    email = input("이메일: ").strip()
    err = validate_required(email, "이메일")
    if err:
        print(err)
        return

    customers = load_data(DATA_FILE)
    customers.append({
        "customer_id": customer_id,
        "customer_name": customer_name,
        "manager_name": manager_name,
        "email": email,
    })
    save_data(DATA_FILE, customers)
    print(f"고객사 {customer_id} 등록 완료.")


def list_all():
    """전체 고객사 목록 출력"""
    customers = load_data(DATA_FILE)
    if not customers:
        print("\n등록된 고객사가 없습니다.")
        return
    print("\n--- 고객사 목록 ---")
    print(f"{'ID':<8} {'고객사명':<20} {'담당자':<12} {'이메일':<30}")
    print("-" * 70)
    for c in customers:
        print(f"{c['customer_id']:<8} {c['customer_name']:<20} {c['manager_name']:<12} {c['email']:<30}")


def detail(customer_id):
    """특정 고객사 상세 조회"""
    customers = load_data(DATA_FILE)
    for c in customers:
        if c["customer_id"] == customer_id:
            print(f"\n--- 고객사 상세 ---")
            print(f"고객사 ID: {c['customer_id']}")
            print(f"고객사명: {c['customer_name']}")
            print(f"담당자명: {c['manager_name']}")
            print(f"이메일: {c['email']}")
            return
    print(f"고객사 {customer_id}를 찾을 수 없습니다.")


def search(keyword):
    """고객사명 또는 담당자명으로 검색"""
    customers = load_data(DATA_FILE)
    results = [
        c for c in customers
        if keyword in c["customer_name"] or keyword in c["manager_name"]
    ]
    if not results:
        print(f"'{keyword}' 검색 결과가 없습니다.")
        return
    print(f"\n--- '{keyword}' 검색 결과 ---")
    print(f"{'ID':<8} {'고객사명':<20} {'담당자':<12} {'이메일':<30}")
    print("-" * 70)
    for c in results:
        print(f"{c['customer_id']:<8} {c['customer_name']:<20} {c['manager_name']:<12} {c['email']:<30}")


def update(customer_id):
    """고객사 정보 수정"""
    customers = load_data(DATA_FILE)
    for c in customers:
        if c["customer_id"] == customer_id:
            print(f"\n--- 고객사 수정 ({customer_id}) ---")
            print(f"현재 고객사명: {c['customer_name']}")
            new_name = input("새 고객사명 (Enter 유지): ").strip()
            if new_name:
                err = validate_required(new_name, "고객사명")
                if err:
                    print(err)
                    return
                c["customer_name"] = new_name

            print(f"현재 담당자명: {c['manager_name']}")
            new_manager = input("새 담당자명 (Enter 유지): ").strip()
            if new_manager:
                err = validate_required(new_manager, "담당자명")
                if err:
                    print(err)
                    return
                c["manager_name"] = new_manager

            print(f"현재 이메일: {c['email']}")
            new_email = input("새 이메일 (Enter 유지): ").strip()
            if new_email:
                err = validate_required(new_email, "이메일")
                if err:
                    print(err)
                    return
                c["email"] = new_email

            save_data(DATA_FILE, customers)
            print(f"고객사 {customer_id} 수정 완료.")
            return
    print(f"고객사 {customer_id}를 찾을 수 없습니다.")


def delete(customer_id):
    """고객사 삭제"""
    customers = load_data(DATA_FILE)
    for i, c in enumerate(customers):
        if c["customer_id"] == customer_id:
            confirm = input(f"고객사 {customer_id} ({c['customer_name']})를 삭제하시겠습니까? (y/n): ").strip().lower()
            if confirm == "y":
                customers.pop(i)
                save_data(DATA_FILE, customers)
                print(f"고객사 {customer_id} 삭제 완료.")
            else:
                print("삭제 취소.")
            return
    print(f"고객사 {customer_id}를 찾을 수 없습니다.")