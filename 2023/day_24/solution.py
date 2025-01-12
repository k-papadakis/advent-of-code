import numpy as np


def read_input(file_path: str) -> list[tuple[list[int], list[int]]]:
    hailstones: list[tuple[list[int], list[int]]] = []
    with open(file_path) as f:
        for line in f:
            p_str, dp_str = line.split("@", maxsplit=1)
            p = list(map(int, p_str.split(",")))
            dp = list(map(int, dp_str.split(",")))
            hailstones.append((p, dp))
    return hailstones


def find_collision_point(
    p: list[int], dp: list[int], q: list[int], dq: list[int]
) -> list[float] | None:
    # p + s dp = q + t dq
    # [dp -dq][s t]^T = q - p
    ap, adp, aq, adq = (np.asarray(v, dtype=np.float64) for v in (p, dp, q, dq))
    sol, residuals, rank, _ = np.linalg.lstsq(np.vstack([adp, -adq]).T, aq - ap)
    if rank < 2 or not np.all(np.isclose(residuals, 0.0)) or not np.all(sol >= 0):
        return None
    return ap + sol[0] * adp  # pyright: ignore[reportAny]


def main():
    import sys

    file_path = sys.argv[1]
    hailstones = read_input(file_path)

    LB, UB = 200000000000000, 400000000000000
    part_1 = 0
    for i in range(len(hailstones)):
        for j in range(i + 1, len(hailstones)):
            p, dp = hailstones[i]
            q, dq = hailstones[j]
            collision_point = find_collision_point(p[:2], dp[:2], q[:2], dq[:2])
            if collision_point is not None and all(
                LB <= x <= UB for x in collision_point
            ):
                part_1 += 1

    print(part_1)


if __name__ == "__main__":
    main()
