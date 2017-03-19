FILL_SHAPE = ((0, 0, 0, 0, 0, 0, 0, 0, 0),
              (0, 0, 0, 1, 1, 1, 0, 0, 0),
              (0, 0, 1, 1, 1, 1, 1, 0, 0),
              (0, 1, 1, 1, 1, 1, 1, 1, 0),
              (0, 1, 1, 1, 1, 1, 1, 1, 0),
              (0, 1, 1, 1, 1, 1, 1, 1, 0),
              (0, 0, 1, 1, 1, 1, 1, 0, 0),
              (0, 0, 0, 1, 1, 1, 0, 0, 0),
              (0, 0, 0, 0, 0, 0, 0, 0, 0))

BORDER_SHAPE = ((0, 0, 0, 1, 1, 1, 0, 0, 0),
                (0, 1, 1, 0, 0, 0, 1, 1, 0),
                (0, 1, 0, 0, 0, 0, 0, 1, 0),
                (1, 0, 0, 0, 0, 0, 0, 0, 1),
                (1, 0, 0, 0, 0, 0, 0, 0, 1),
                (1, 0, 0, 0, 0, 0, 0, 0, 1),
                (0, 1, 0, 0, 0, 0, 0, 1, 0),
                (0, 1, 1, 0, 0, 0, 1, 1, 0),
                (0, 0, 0, 1, 1, 1, 0, 0, 0))


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
    img.show()


def draw_image(data):
    instructions = {
        "00": draw_dots,
        "01": draw_dots,
        "10": draw_dots,
        "11": draw_dots
    }
    instructions[data["TYPE"]]()


def extract_data(bin_hash):
    """Create data dictionary from hash string of length 160.

    Details:
    Duplicate the hash (new length: 320).
    0 - 305: DOT_DATA, 61 Strings of length 5.
    305 - 310: PALETTE.
    310 - 312 BG.
    312 - 314 TYPE.
    Last 6 characters are currently not used.
    """
    bin_hash *= 2
    extracted_data = {}
    dot_string = bin_hash[0:305]
    dot_list = [dot_string[i:i + 5] for i in range(0, len(dot_string), 5)]

    extracted_data["DOT_DATA"] = dot_list
    extracted_data["PALETTE"] = bin_hash[305:310]
    extracted_data["BG"] = bin_hash[310:312]
    extracted_data["TYPE"] = bin_hash[312:314]

    return extracted_data


def hex_to_bin(hex_string):
    """Convert hex to binary string."""
    length = 160  # hash length * bits per hex number
    return str(bin(int(hex_string, 16))[2:].zfill(length))


def hex_to_rgb(hex_string):
    """Convert hex string to rgb tuple"""
    parts = (hex_string[i: i + 2] for i in range(0, len(hex_string), 2))
    return [int(part, 16) for part in parts]


KEYS = ("000", "001", "010", "011", "100", "101", "110", "111")

PALETTES = ()

BG_PALETTES = ()


def make_palette(data):
    assert (len(KEYS) == len(PALETTES)), \
        "KEYS and PALETTES must have same length"

    p_index = int(data["PALETTE"], 2)
    assert (len(KEYS) >= p_index), \
        "KEYS and PALETTES do not meet requirements, see app.extract_data"

    bg_index = int(data["BG"], 2)
    assert (len(BG_PALETTES) >= bg_index), \
        "BG_PALETTES does not meet requirements, see app.extract_data"

    colors = PALETTES[p_index]
    bg = BG_PALETTES[p_index][bg_index]

    palette = {}
    for i, key in enumerate(KEYS):
        palette[key] = colors[i]
    palette["BG"] = bg

    return palette
