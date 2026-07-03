from storageai import print_multiplication_table


def get_positive_int(prompt):
    """Prompt the user until a positive integer is entered."""
    while True:
        raw = input(prompt).strip()
        if not raw:
            print("입력값이 없습니다. 숫자를 입력해주세요.")
            continue
        try:
            value = int(raw)
        except ValueError:
            print("잘못된 입력입니다. 정수를 입력해주세요.")
            continue
        if value < 1:
            print("1 이상의 값을 입력해주세요.")
            continue
        return value


def main():
    print("=== 구구단 출력 프로그램 ===\n")

    start = get_positive_int("시작 단을 입력하세요 (예: 2): ")
    end = get_positive_int("끝 단을 입력하세요 (예: 9): ")

    if start > end:
        print(f"시작 단({start})이 끝 단({end})보다 큽니다. 종료합니다.")
        return

    repeat_count = get_positive_int("반복 횟수를 입력하세요 (예: 9): ")

    print()
    print_multiplication_table(start, end, repeat_count)


if __name__ == "__main__":
    main()