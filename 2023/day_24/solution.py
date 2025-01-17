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


def find_num_collissions(hailstones: list[tuple[list[float], list[float]]]) -> int:
    LB, UB = 200_000_000_000_000, 400_000_000_000_000
    num_collissions = 0
    for i in range(len(hailstones)):
        for j in range(i + 1, len(hailstones)):
            p, dp = hailstones[i]
            q, dq = hailstones[j]
            collision_point = find_collision_point(p[:2], dp[:2], q[:2], dq[:2])
            if collision_point is not None and all(
                LB <= x <= UB for x in collision_point
            ):
                num_collissions += 1
    return num_collissions


def cross_prod(u: list[float], v: list[float]) -> list[float]:
    return [
        u[1] * v[2] - u[2] * v[1],
        u[2] * v[0] - u[0] * v[2],
        u[0] * v[1] - u[1] * v[0],
    ]


def generate_system(
    p1: list[float], dp1: list[float], p2: list[float], dp2: list[float]
) -> tuple[list[list[float]], list[float]]:
    c = [a - b for a, b in zip(cross_prod(p1, dp1), cross_prod(p2, dp2))]
    a = [b - a for a, b in zip(dp1, dp2)]
    b = [a - b for a, b in zip(p1, p2)]
    mat = [
        [0, -a[2], a[1], 0, -b[2], b[1]],
        [a[2], 0, -a[0], b[2], 0, -b[0]],
        [-a[1], a[0], 0, -b[1], b[0], 0],
    ]
    return mat, c


def find_rock(
    hailstones: list[tuple[list[float], list[float]]],
) -> tuple[list[int], list[int]]:
    # We want to find q, dq given that
    # q + t dq = p + t dp for all p, dp
    # This is equivalent to:
    # q - p parallel to dp - dq for all p, dp
    # (q - p) x (dp - dq) = 0 for all p, dp
    # q x dp - q x dq - p x dp + p x dq = 0 for all p, dp
    # q x dp - p x dp + p x dq = q x dq  for all p, dp
    # Equate a pair of (p1, dp1), (p2, dp2)
    # q x dp1 - p1 x dp1 + p1 x dq = q x dp2 - p2 x dp2 + p2 x dq
    # (dp2 - dp1) x q + (p1 - p2) x dq = p1 x dp1 - p2 x dp2
    # a x q + b x dq = c
    # a2 q3 - a3 q2 + b2 dq3 - b3 dq2 = c1
    # a3 q1 - a1 q3 + b3 dq1 - b1 dq3 = c2
    # a1 q2 - a2 q1 + b1 dq2 - b2 dq1 = c3
    # The matrix is:
    #   0 -a3  a2   0 -b3  b2
    #  a3   0 -a1  b3   0 -b1
    # -a2  a1   0 -b2  b1   0
    # Pick another pair to make 3 more linear equations.
    # Solve the system.

    (p1, dp1), (p2, dp2), (p3, dp3) = hailstones[:3]
    mat1, c1 = generate_system(p1, dp1, p2, dp2)
    mat2, c2 = generate_system(p1, dp1, p3, dp3)
    mat = mat1 + mat2
    c = c1 + c2

    sol_approx = unique_solve(mat, c)
    assert sol_approx is not None
    sol = list(map(round, sol_approx))
    q, dq = sol[:3], sol[3:]
    return q, dq


def main():
    import sys

    file_path = sys.argv[1]
    hailstones = read_input(file_path)
    part_1 = find_num_collissions(hailstones)
    part_2 = sum(find_rock(hailstones)[0])
    print(f"{part_1 = }, {part_2 =}")


if __name__ == "__main__":
    main()
