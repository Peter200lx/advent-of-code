from pathlib import Path


def chunk_list(in_list, width, height):
    total_pixels = width * height
    assert len(in_list) % total_pixels == 0
    for i in range(len(in_list) // total_pixels):
        yield in_list[i * total_pixels : (i + 1) * total_pixels]


def render_layers(in_list, width, height):
    final_image = [[2 for _ in range(width)] for _ in range(height)]
    for layer in chunk_list(in_list, width, height):
        for y, row in enumerate(
            layer[i * width : (i + 1) * width] for i in range(height)
        ):
            for x, value in enumerate(row):
                if final_image[y][x] == 2:
                    final_image[y][x] = value
    return final_image


if __name__ == "__main__":
    DATA = Path("day08.input").read_text().strip()
    int_list = [int(c) for c in DATA]
    WIDTH = 25
    HEIGHT = 6
    fewest_zero = min((l.count(0), l) for l in chunk_list(int_list, WIDTH, HEIGHT))
    print(fewest_zero[1].count(1) * fewest_zero[1].count(2))
    for row in render_layers(int_list, WIDTH, HEIGHT):
        print("".join("X" if i else " " for i in row))
