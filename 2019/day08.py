from pathlib import Path

INPUT_FILE = Path(__file__).with_suffix(".input")


def chunk_list(in_list, width, height):
    total_pixels = width * height
    assert len(in_list) % total_pixels == 0
    for i in range(0, len(in_list), total_pixels):
        yield in_list[i : i + total_pixels]


def render_layers(in_list, width, height):
    final_image = [[2 for _ in range(width)] for _ in range(height)]
    for layer in chunk_list(in_list, width, height):
        for y, row in enumerate(
            layer[i : i + width] for i in range(0, height * width, width)
        ):
            for x, value in enumerate(row):
                if final_image[y][x] == 2:
                    final_image[y][x] = value
    return final_image


if __name__ == "__main__":
    DATA = INPUT_FILE.read_text().strip()
    int_list = [int(c) for c in DATA]
    WIDTH = 25
    HEIGHT = 6
    _, fewest_zero = min((l.count(0), l) for l in chunk_list(int_list, WIDTH, HEIGHT))
    print(fewest_zero.count(1) * fewest_zero.count(2))
    for line in render_layers(int_list, WIDTH, HEIGHT):
        print("".join("#" if i else " " for i in line))
