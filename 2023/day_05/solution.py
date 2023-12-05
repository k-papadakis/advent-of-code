import re
from dataclasses import dataclass


@dataclass
class RangeMap:
    destination_range_start: int
    source_range_start: int
    range_length: int

    def __contains__(self, key: int) -> bool:
        return 0 <= (key - self.source_range_start) < self.range_length

    def __getitem__(self, key: int) -> int:
        if key in self:
            return self.destination_range_start + (key - self.source_range_start)
        else:
            raise KeyError(key)

    @classmethod
    def from_string(cls, range_map_str: str) -> "RangeMap":
        return cls(*map(int, range_map_str.split()))


@dataclass
class RangeMapCollection:
    source_category: str
    target_category: str
    range_maps: list[RangeMap]

    def __getitem__(self, key: int) -> int:
        for range_map in self.range_maps:
            if key in range_map:
                return range_map[key]
        return key

    @classmethod
    def from_string(cls, range_map_collection_str: str) -> "RangeMapCollection":
        match = re.match(
            r"(?P<source_category>.*?)-to-(?P<target_category>.*?) map:\n(?P<range_maps>.*)",
            range_map_collection_str,
            re.DOTALL,
        )
        if not match:
            raise ValueError("Could not match pattern.")

        range_maps = [
            RangeMap.from_string(range_map_str)
            for range_map_str in match["range_maps"].splitlines()
        ]
        return cls(match["source_category"], match["target_category"], range_maps)


@dataclass
class Almanac:
    range_map_collections: list[RangeMapCollection]

    def __getitem__(self, key: int) -> int:
        res = key
        for range_map_collection in self.range_map_collections:
            res = range_map_collection[res]
        return res

    @classmethod
    def from_string(cls, almanac_str: str) -> "Almanac":
        almanac = cls(
            [
                RangeMapCollection.from_string(range_map_collection_str)
                for range_map_collection_str in almanac_str.split("\n\n")
            ]
        )
        return almanac


def read_input() -> tuple[list[int], Almanac]:
    with open("input.txt") as f:
        seeds_str = f.readline()
        f.readline()
        almanac_str = f.read()

    seeds = list(map(int, seeds_str.lstrip("seeds:").split()))
    almanac = Almanac.from_string(almanac_str)

    return seeds, almanac


def main() -> None:
    seeds, almanac = read_input()
    part_1 = min(almanac[seed] for seed in seeds)
    print(f"{part_1 = }")


if __name__ == "__main__":
    main()
