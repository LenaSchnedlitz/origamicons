def sha1_hash(username):
    """Return SHA-1 hash of passed username as string of zeros and ones."""

    def hex_to_bin(sha_hash):
        """Convert SHA-1 (hex) hash to binary number string."""
        length = 160  # hash length * bits per hex number
        return str(bin(int(sha_hash, 16))[2:].zfill(length))

    from hashlib import sha1
    sha = sha1()
    sha.update(str.encode(username))
    hex_hash = sha.hexdigest()
    return hex_to_bin(hex_hash)


def extract_data(bin_hash):
    """Create data dictionary from hash string of length 160.

    Details:
    Duplicate the hash (new length: 320).
    0 - 305: DOT_DATA, 61 Strings of length 5.
    305 - 310: PALETTE.
    310 - 312 BG.
    312 - 314 SHAPE.
    Last 6 characters are currently not used.
    """
    bin_hash *= 2
    extracted_data = {}
    dot_string = bin_hash[0:305]
    dot_list = [dot_string[i:i + 5] for i in range(0, len(dot_string), 5)]

    extracted_data["DOT_DATA"] = dot_list
    extracted_data["PALETTE"] = bin_hash[305:310]
    extracted_data["BG"] = bin_hash[310:312]
    extracted_data["SHAPE"] = bin_hash[312:314]

    return extracted_data


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

    fill_shape = ((0, 0, 0, 0, 0, 0, 0, 0, 0),
                  (0, 0, 0, 1, 1, 1, 0, 0, 0),
                  (0, 0, 1, 1, 1, 1, 1, 0, 0),
                  (0, 1, 1, 1, 1, 1, 1, 1, 0),
                  (0, 1, 1, 1, 1, 1, 1, 1, 0),
                  (0, 1, 1, 1, 1, 1, 1, 1, 0),
                  (0, 0, 1, 1, 1, 1, 1, 0, 0),
                  (0, 0, 0, 1, 1, 1, 0, 0, 0),
                  (0, 0, 0, 0, 0, 0, 0, 0, 0))

    border_shape = ((0, 0, 0, 1, 1, 1, 0, 0, 0),
                    (0, 1, 1, 0, 0, 0, 1, 1, 0),
                    (0, 1, 0, 0, 0, 0, 0, 1, 0),
                    (1, 0, 0, 0, 0, 0, 0, 0, 1),
                    (1, 0, 0, 0, 0, 0, 0, 0, 1),
                    (1, 0, 0, 0, 0, 0, 0, 0, 1),
                    (0, 1, 0, 0, 0, 0, 0, 1, 0),
                    (0, 1, 1, 0, 0, 0, 1, 1, 0),
                    (0, 0, 0, 1, 1, 1, 0, 0, 0))

    resolution = len(fill_shape)
    distance = (size - 2 * margin) // resolution
    coords = [margin + distance // 2 + i * distance for i in range(resolution)]

    fill_tuples = map_tuples(fill_shape, coords)
    border_tuples = map_tuples(border_shape, coords)

    return fill_tuples, border_tuples


def draw_dots():
    from PIL import Image, ImageDraw
    img = Image.new('RGBA', (250, 250), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    r = 9
    s = 8
    fill, border = calculate_dot_positions()
    for i, (x, y) in enumerate(fill):
        draw.ellipse((x - r, y - r, x + r, y + r), fill=(255, 0, 0, 0))
    for i, (x, y) in enumerate(border):
        draw.ellipse((x - s, y - s, x + s, y + s), fill=(255, 255, 0, 0))
    img.show()


name_hash = sha1_hash("mailea")
data = extract_data(name_hash)

draw_dots()
