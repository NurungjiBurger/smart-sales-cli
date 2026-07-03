import customer
import report
import exporter


def print_menu():
    print("\n" + "=" * 40)
    print("          Smart Sales CLI")
    print("=" * 40)
    print(" 1. 고객사 등록")
    print(" 2. 고객사 목록")
    print(" 3. 고객사 상세 조회")
    print(" 4. 고객사 검색")
    print(" 5. 고객사 수정")
    print(" 6. 고객사 삭제")
    print(" 7. 영업일지 등록")
    print(" 8. 영업일지 목록")
    print(" 9. 영업일지 수정")
    print("10. 영업일지 상신")
    print("11. 영업일지 승인")
    print("12. 영업일지 반려")
    print("13. 영업일지 회수")
    print("14. 고객사별 활동 요약")
    print("15. 고객사 목록 CSV 내보내기")
    print(" 0. 종료")
    print("-" * 40)


def main():
    while True:
        print_menu()
        choice = input("메뉴를 선택하세요: ").strip()

        if choice == "1":
            customer.register()
        elif choice == "2":
            customer.list_all()
        elif choice == "3":
            cid = input("고객사 ID: ").strip()
            customer.detail(cid)
        elif choice == "4":
            keyword = input("검색어: ").strip()
            customer.search(keyword)
        elif choice == "5":
            cid = input("고객사 ID: ").strip()
            customer.update(cid)
        elif choice == "6":
            cid = input("고객사 ID: ").strip()
            customer.delete(cid)
        elif choice == "7":
            report.register()
        elif choice == "8":
            report.list_all()
        elif choice == "9":
            rid = input("영업일지 ID: ").strip()
            report.update(rid)
        elif choice == "10":
            rid = input("영업일지 ID: ").strip()
            report.submit(rid)
        elif choice == "11":
            rid = input("영업일지 ID: ").strip()
            report.approve(rid)
        elif choice == "12":
            rid = input("영업일지 ID: ").strip()
            report.reject(rid)
        elif choice == "13":
            rid = input("영업일지 ID: ").strip()
            report.withdraw(rid)
        elif choice == "14":
            report.summary_by_customer()
        elif choice == "15":
            exporter.export_customers_csv()
        elif choice == "0":
            print("프로그램을 종료합니다.")
            break
        else:
            print("잘못된 입력입니다. 0~14 사이의 숫자를 입력해주세요.")


if __name__ == "__main__":
    main()