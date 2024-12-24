import re
import sys


def read_input(
    file_path: str,
) -> tuple[dict[str, bool], list[tuple[str, str, str, str]]]:
    with open(file_path) as f:
        s = f.read()

    # nodes
    wires: dict[str, bool] = {
        m[1]: m[2] == "1" for m in re.finditer(r"(\w+): (1|0)", s)
    }

    # edges
    gates: list[tuple[str, str, str, str]] = [
        (m[1], m[2], m[3], m[4])
        for m in re.finditer(r"(\w+) (AND|OR|XOR) (\w+) -> (\w+)", s)
    ]

    return wires, gates


def compute_z(wires: dict[str, bool], gates: list[tuple[str, str, str, str]]):
    all_wires = set(wires)
    for x, _, y, z in gates:
        all_wires.update((x, y, z))

    final_nodes = sorted((x for x in all_wires if x.startswith("z")), reverse=True)
    done: set[str] = set()
    while len(done) < len(final_nodes):
        for x, op, y, z in gates:
            if x not in wires or y not in wires:
                continue

            match op:
                case "AND":
                    wires[z] = wires[x] and wires[y]
                case "OR":
                    wires[z] = wires[x] or wires[y]
                case "XOR":
                    wires[z] = wires[x] != wires[y]
                case other:
                    raise ValueError(f"Invalid op {other}")

            if z.startswith("z"):
                done.add(z)

    res = 0
    for z in final_nodes:
        res <<= 1
        res += wires[z]
    return res


def main():
    file_path = sys.argv[1]
    wires, gates = read_input(file_path)
    part_1 = compute_z(wires, gates)
    print(part_1)


if __name__ == "__main__":
    main()
