# /// script
# requires-python = ">=3.14"
# dependencies = [
#     "matplotlib>=3.10.8",
#     "networkx>=3.6.1",
#     "scipy>=1.16.3",
# ]
# ///


import sys
from pathlib import Path

import matplotlib.pyplot as plt
import networkx as nx


def parse(contents: str) -> list[tuple[str, str]]:
    edges: list[tuple[str, str]] = []
    for line in contents.splitlines():
        u, vs = line.split(":", 1)
        u = u.strip()
        for v in vs.split():
            edges.append((u.strip(), v.strip()))
    return edges


def main():
    file_path = sys.argv[1]
    contents = Path(file_path).read_text()
    edges = parse(contents)
    graph = nx.Graph(edges)
    node_color = [
        "#ff0000" if node in {"svr", "out", "fft", "dac", "you"} else "#1f78b4"
        for node in graph.nodes
    ]
    nx.draw(graph, with_labels=True, node_color=node_color)
    plt.show()


if __name__ == "__main__":
    main()
