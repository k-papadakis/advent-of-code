import re
import sys


def read_input(
    file_path: str,
) -> tuple[dict[str, bool], list[tuple[str, str, str, str]]]:
    with open(file_path) as f:
        s = f.read()

    wires: dict[str, bool] = {
        m[1]: m[2] == "1" for m in re.finditer(r"(\w+): (1|0)", s)
    }

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


def traverse(gates_list: list[tuple[str, str, str, str]]) -> set[tuple[str, str]]:
    # https://www.ece.uvic.ca/~fayez/courses/ceng465/lab_465/project1/adders.pdf
    swapped: set[tuple[str, str]] = set()
    gates = {(a, op, b): c for a, op, b, c in gates_list} | {
        (b, op, a): c for a, op, b, c in gates_list
    }

    def swap(c: str, cc: str) -> None:
        for k, v in gates.items():
            if v == c:
                gates[k] = cc
                if (cc, c) not in swapped:
                    swapped.add((c, cc))
            elif v == cc:
                gates[k] = c
                if (c, cc) not in swapped:
                    swapped.add((cc, c))

    def get(a: str, op: str, b: str) -> str:
        # Assuming that at most one of the gate's inputs is wrong.
        if (a, op, b) in gates:
            return gates[a, op, b]

        for (aa, oop, bb), cc in gates.items():
            if oop == op and aa == a:
                swap(b, bb)
                return cc
            elif oop == op and bb == b:
                swap(a, aa)
                return cc

        raise ValueError(f"Could not get {(a, op, b)}")

    c_in: str | None = None
    for i in range(45):
        x = f"x{i:02d}"
        y = f"y{i:02d}"
        z = f"z{i:02d}"

        p = get(x, "XOR", y)
        g = get(x, "AND", y)

        if c_in is None:
            pc = p
            c_out = g
            s = p
        else:
            pc = get(p, "AND", c_in)
            c_out = get(g, "OR", pc)
            s = get(p, "XOR", c_in)
        c_in = c_out

    return swapped


def main():
    file_path = sys.argv[1]
    wires, gates = read_input(file_path)
    part_1 = compute_z(wires, gates)
    part_2 = ",".join(sorted(c for t in traverse(gates) for c in t))
    print(f"part_1 = {part_1} part_2 = {part_2}")


if __name__ == "__main__":
    main()
