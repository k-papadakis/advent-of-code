def read_input(path: str) -> list[str]:
    with open(path) as f:
        s = f.read()
    return s.splitlines()


grid = read_input("input.txt")
m, n = len(grid), len(grid[0])
cur = [-1] * n
res = 0

for i in range(m):
    for j in range(n):
        match grid[i][j]:
            case "O":
                cur[j] += 1
                res += m - cur[j]
            case "#":
                cur[j] = i
            case ".":
                pass
            case _:
                raise ValueError(f"Unknown symbol {grid[i][j]}")
print(res)
