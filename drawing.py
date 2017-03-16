def calculate_dot_positions(margin=8, size=250):
    """Map shapes to canvas size. Return coordinate tuples."""

    def map_tuples(shape, coordinates):
        """Map shape of 1s to coordinate system."""
        tuples = []
        for i, row in enumerate(shape):
            for j, cell in enumerate(row):
                if cell:
                    tuples.append((coordinates[i], coordinates[j]))
        return tuples

    from data import FILL_SHAPE, BORDER_SHAPE

    resolution = len(FILL_SHAPE)
    distance = (size - 2 * margin) // resolution
    coords = [margin + distance // 2 + i * distance for i in range(resolution)]

    fill_tuples = map_tuples(FILL_SHAPE, coords)
    border_tuples = map_tuples(BORDER_SHAPE, coords)

    return fill_tuples, border_tuples


def draw_dots():
    from PIL import Image, ImageDraw
    img = Image.new('RGBA', (250, 250), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    rf = 9
    rb = 8
    fill, border = calculate_dot_positions()
    for i, (x, y) in enumerate(fill):
        draw.ellipse((x - rf, y - rf, x + rf, y + rf), fill=(255, 0, 0, 0))
    for i, (x, y) in enumerate(border):
        draw.ellipse((x - rb, y - rb, x + rb, y + rb), fill=(255, 255, 0, 0))


def draw_image(data):
    instructions = {
        "00": draw_dots,
        "01": draw_dots,
        "10": draw_dots,
        "11": draw_dots
    }
    instructions[data["TYPE"]]()
