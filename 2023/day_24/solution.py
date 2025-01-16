from copy import deepcopy


def read_input(file_path: str) -> list[tuple[list[float], list[float]]]:
    hailstones: list[tuple[list[float], list[float]]] = []
    with open(file_path) as f:
        for line in f:
            p_str, dp_str = line.split("@", maxsplit=1)
            p = list(map(float, p_str.split(",")))
            dp = list(map(float, dp_str.split(",")))
            hailstones.append((p, dp))
    return hailstones


def row_echelon(
    a: list[list[float]], b: list[float]
) -> tuple[list[list[float]], list[float]]:
    a = deepcopy(a)
    b = deepcopy(b)
    m, n = len(a), len(a[0])
    h, k = 0, 0
    while h < m and k < n:
        i_max = max(range(h, m), key=lambda i: abs(a[i][k]))
        if a[i_max][k] == 0:
            k += 1
            continue
        a[h], a[i_max] = a[i_max], a[h]
        b[h], b[i_max] = b[i_max], b[h]
        for i in range(h + 1, m):
            f = a[i][k] / a[h][k]
            a[i][k] = 0
            for j in range(k + 1, n):
                a[i][j] -= a[h][j] * f
            b[i] -= b[h] * f
        h += 1
        k += 1
    return a, b


def unique_solve(a: list[list[float]], b: list[float]) -> list[float] | None:
    assert len(a) == len(b)
    m, n = len(a), len(a[0])
    if m < n:
        return None
    a, b = row_echelon(a, b)
    if any(a[i][i] == 0 for i in range(n)):
        return None
    sol = [float("nan")] * n
    sol[n - 1] = b[n - 1] / a[n - 1][n - 1]
    for i in reversed(range(n - 1)):
        sol[i] = (b[i] - sum(a[i][j] * sol[j] for j in range(i + 1, n))) / a[i][i]
    return sol


def find_collision_point(
    p: list[float], dp: list[float], q: list[float], dq: list[float]
) -> list[float] | None:
    # p + s dp = q + t dq
    # [dp -dq][s t]^T = q - p
    n = len(p)
    a = [[dp[i], -dq[i]] for i in range(n)]
    b = [q[i] - p[i] for i in range(n)]
    ts = unique_solve(a, b)
    if ts is None or ts[0] < 0 or ts[1] < 0:
        return None
    return [p[i] + ts[0] * dp[i] for i in range(len(p))]


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
