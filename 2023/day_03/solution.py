# %%
def read_input() -> list[list[str]]:
    with open("input.txt") as f:
        return [list(line) for line in f.read().splitlines()]


arr = read_input()

m = len(arr)
n = len(arr[0])


def issymbol(s: str) -> bool:
    return len(s) == 1 and s != "." and not s.isdigit()


# %%
res: int = 0
start: tuple[int, int] | None = None
bordering: bool = False

for i in range(m):
    if start and bordering:
        res += int("".join(arr[start[0]][start[1] :]))
    start = None
    bordering = False

    for j in range(n):
        if arr[i][j].isdigit():
            if not start:
                start = i, j

            if not bordering:
                for k, l in (
                    (i - 1, j),
                    (i + 1, j),
                    (i, j - 1),
                    (i, j + 1),
                    (i + 1, j + 1),
                    (i - 1, j - 1),
                    (i - 1, j + 1),
                    (i + 1, j - 1),
                ):
                    if 0 <= k < m and 0 <= l < n:
                        if issymbol(arr[k][l]):
                            bordering = True
        else:
            if start and bordering:
                res += int("".join(arr[start[0]][start[1] : j]))
            start = None
            bordering = False
print(res)

# %%
