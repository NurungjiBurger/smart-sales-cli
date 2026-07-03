def print_multiplication_table(start=2, end=9, repeat_count=9):
    """Print the multiplication table from `start` to `end`, each repeated `repeat_count` times."""
    for i in range(start, end + 1):
        for j in range(1, repeat_count + 1):
            print(f"{i} x {j} = {i * j:2d}")
        print()  # blank line between each dan


if __name__ == "__main__":
    print_multiplication_table()