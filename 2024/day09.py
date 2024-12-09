from pathlib import Path

INPUT_FILE = Path(__file__).with_suffix(".input")


class DiskMap:
    def __init__(self, raw_input: str):
        blocks = []
        chunks = []
        cur_id = 0
        for i, c in enumerate(raw_input):
            d = int(c)
            if i % 2 == 0:
                blocks += [cur_id] * d
                chunks.append((cur_id, d))
                cur_id += 1
            else:
                blocks += [None] * d
                chunks.append((None, d))
        self.blocks = blocks
        self.chunks = chunks

    def p1(self) -> int:
        blocks = list(self.blocks)
        end = len(blocks) - 1
        for i, cur_id in enumerate(blocks):
            if cur_id is not None:
                continue
            while blocks[end] is None:
                end -= 1
            if i >= end:
                break
            blocks[i], blocks[end] = blocks[end], blocks[i]
        return sum(i * c for i, c in enumerate(blocks) if c is not None)

    def p2(self) -> int:
        chunks = list(self.chunks)
        for last in range(-1, -len(chunks), -1):
            end_index = len(chunks) + last
            cur_id, size = chunks[last]
            if cur_id is None:
                continue
            start = 0
            while start < end_index and not (
                chunks[start][0] is None and chunks[start][1] >= size
            ):
                start += 1
            if start >= end_index:
                continue
            _none, to_fill_size = chunks[start]
            if to_fill_size == size:
                chunks[start] = (cur_id, size)
                chunks[last] = (None, size)
            elif to_fill_size > size:
                chunks[start] = (cur_id, size)
                chunks.insert(start + 1, (None, to_fill_size - size))
                chunks[last] = (None, size)
            else:
                raise ValueError
        blocks = []
        for cur_id, size in chunks:
            blocks += [cur_id] * size
        return sum(i * c for i, c in enumerate(blocks) if c is not None)


if __name__ == "__main__":
    DATA = INPUT_FILE.read_text().strip()
    DISK = DiskMap(DATA)

    print(DISK.p1())
    print(DISK.p2())
