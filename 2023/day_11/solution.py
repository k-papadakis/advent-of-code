from itertools import combinations, pairwise


def read_input(path: str) -> list[str]:
    with open(path) as f:
        s = f.read()
    grid = s.splitlines()
    return grid


grid = read_input("input.txt")
m, n = len(grid), len(grid[0])

i_map = []
shift = 0
for i in range(m):
    if all(grid[i][j] == "." for j in range(n)):
        shift += 1
    i_map.append(i + shift)

j_map = []
shift = 0
for j in range(n):
    if all(grid[i][j] == "." for i in range(m)):
        shift += 1
    j_map.append(j + shift)

i_coords, j_coords = [], []
for i in range(m):
    for j in range(n):
        if grid[i][j] == "#":
            i_coords.append(i_map[i])
            j_coords.append(j_map[j])
            
# Up to here it's correct


# res = sum(k * (b - a) for k, (a, b) in enumerate(pairwise(sorted(i_coords)), 1)) + sum(
#     k * (b - a) for k, (a, b) in enumerate(pairwise(sorted(j_coords)), 1)
# )
# print(res)

res = sum(abs(i2 - i1) + abs(j2 - j1) for (i1, j1), (i2, j2) in combinations(zip(i_coords, j_coords), 2))
print(res)
