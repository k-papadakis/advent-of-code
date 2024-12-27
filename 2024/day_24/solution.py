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
    # part_1 = compute_z(wires, gates)
    # print(part_1)

    # https://www.ece.uvic.ca/~fayez/courses/ceng465/lab_465/project1/adders.pdf
    gates = {(a, op, b): c for a, op, b, c in gates} | {
        (b, op, a): c for a, op, b, c in gates
    }
    c_in: str | None = None
    for i in range(45):
        x = f"x{i:02d}"
        y = f"y{i:02d}"
        z = f"z{i:02d}"

        p = gates[x, "XOR", y]
        g = gates[x, "AND", y]

        if c_in is None:
            pc = p
            c_out = g
            s = p
        else:
            pc = gates[p, "AND", c_in]
            c_out = gates[g, "OR", pc]
            s = gates[p, "XOR", c_in]
            if s != z:
                raise ValueError(f"{s=} {z=}")
        c_in = c_out


# c_out at iteration 12 was z12,
# so there was a broken c_in at iteration 13.
# s should have been z12 at iteration 12,
# but it was fgc.
# Swap fgc and z12
#
# pc was z29 at iteration 29,
# so c_out was broken at the same iteration.
# Assume that g was ok (=wbg).
# Let's look for "wbg OR" or "OR wbg"
# the other part of "OR" is going to be the correct pc.
# A match was found and it was `wbg OR mtj -> gdv`,
# so pc should be mtj,
# and mtj should be swapped with z29.
#
# At iteration 33, pc was broken.
# Its inputs were "p=vvm AND c_in=rrd".
# Let's look for "vvm AND" or "AND rrd".
# A match was found and it was "dgr AND rrd -> vtc".
# So, dgr and vvm should be swapped.
#
# At iteration 37, c_out was broken.
# Its inputs were "g=z37 OR pc=wjd".
# Let's look for "OR wjd".
# A match was found and it was "wjd OR dtv -> jkb".
# So, swap z37 and dtv.


if __name__ == "__main__":
    main()
