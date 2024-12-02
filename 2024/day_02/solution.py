import sys
from os import PathLike


def read_input(file: str | PathLike[str]) -> list[list[int]]:
    with open(file) as f:
        lines = f.readlines()
    reports = [list(map(int, line.split())) for line in lines]
    return reports


def is_safe_asc(report: list[int], tolerate: bool) -> bool:
    for i in range(1, len(report)):
        if not 1 <= report[i] - report[i - 1] <= 3:
            return tolerate and (
                is_safe_asc(
                    report[i - 1 : i] + report[i + 1 :],
                    tolerate=False,
                )
                or is_safe_asc(
                    report[i - 2 : i - 1] + report[i:],
                    tolerate=False,
                )
            )
    return True


def is_safe(report: list[int], tolerate: bool) -> bool:
    return is_safe_asc(report, tolerate) or is_safe_asc(report[::-1], tolerate)


def main() -> None:
    file = sys.argv[1]
    reports = read_input(file)
    part_1 = sum(is_safe(report, tolerate=False) for report in reports)
    part_2 = sum(is_safe(report, tolerate=True) for report in reports)
    print(f"{part_1 = } {part_2 = }")


if __name__ == "__main__":
    main()
