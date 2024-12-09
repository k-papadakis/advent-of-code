from collections import deque
import sys
from dataclasses import dataclass
from typing import Self, override
from collections.abc import Sequence


@dataclass(slots=True)
class File:
    id: int
    size: int


@dataclass(slots=True)
class MemoryBlock:
    files: deque[File]
    remaining: int


def sum_range(start: int, stop: int) -> int:
    small = (start - 1) * start // 2
    big = stop * (stop + 1) // 2
    return big - small


@dataclass(slots=True)
class Disk:
    blocks: Sequence[MemoryBlock]

    def compact_with_frag(self) -> None:
        i = 0
        j = len(self.blocks) - 1

        while i < j:
            first_block = self.blocks[i]
            last_block = self.blocks[j]

            if first_block.remaining == 0:
                i += 1
                continue

            if not last_block.files:
                j -= 1
                continue

            last_file_size = last_block.files[-1].size

            if last_file_size <= first_block.remaining:
                first_block.files.append(last_block.files.pop())
                first_block.remaining -= last_file_size
                last_block.remaining += last_file_size
            else:
                first_block.files.append(
                    File(id=last_block.files[-1].id, size=first_block.remaining)
                )
                last_block.files[-1].size -= first_block.remaining
                last_block.remaining += first_block.remaining
                first_block.remaining = 0

    def compact_without_frag(self) -> None:
        for j in reversed(range(1, len(self.blocks))):
            for i in range(j):
                last_file_size = self.blocks[j].files[0].size
                if last_file_size <= self.blocks[i].remaining:
                    self.blocks[i].files.append(self.blocks[j].files.popleft())
                    self.blocks[i].remaining -= last_file_size
                    self.blocks[j - 1].remaining += last_file_size
                    break

    def checksum(self) -> int:
        res = 0
        file_start = 0
        for block in self.blocks:
            for file in block.files:
                file_end = file_start + file.size - 1
                res += sum_range(file_start, file_end) * file.id
                file_start += file.size
            file_start += block.remaining
        return res

    @classmethod
    def from_seq(cls, seq: Sequence[int]) -> Self:
        blocks: list[MemoryBlock] = []
        n = len(seq)
        for i in range(0, n, 2):
            remaining = seq[i + 1] if i + 1 < n else 0
            blocks.append(
                MemoryBlock(
                    files=deque([File(id=i // 2, size=seq[i])]),
                    remaining=remaining,
                )
            )
        return cls(blocks)

    @override
    def __str__(self) -> str:
        lst: list[str] = []
        for block in self.blocks:
            for file in block.files:
                lst.append(f"{file.id}" * file.size)
            lst.append("." * block.remaining)
        return "".join(lst)


def read_input(file_path: str) -> list[int]:
    with open(file_path) as f:
        disk_string = f.read().rstrip()
    disk_list = list(map(int, disk_string))
    return disk_list


def main():
    file_path = sys.argv[1]
    disk_list = read_input(file_path)

    disk = Disk.from_seq(disk_list)
    disk.compact_with_frag()
    part_1 = disk.checksum()

    disk = Disk.from_seq(disk_list)
    disk.compact_without_frag()
    part_2 = disk.checksum()

    print(f"{part_1 = } {part_2 = }")


if __name__ == "__main__":
    main()
