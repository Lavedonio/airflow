import sys


def main(exit_status: int) -> None:
    print("This is a Python test script.")
    assert exit_status == 0, "Exit status is not 0"
    print("Passed validation.")


if __name__ == '__main__':
    try:
        exit_status = int(sys.argv[1])
    except (IndexError, ValueError):
        exit_status = 0

    main(exit_status)
