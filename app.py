def sha1_hash(username):
    """Return SHA-1 hash of passed username."""
    from hashlib import sha1
    sha = sha1()
    sha.update(str.encode(username))
    return sha.hexdigest()


def hex_to_coordinates(hex_string):
    """Convert hex string to (x, y) - coordinate tuples.

    Two digits represent one value -> 4 digits per (x, y) tuple.
    After the split, hex numbers are converted to decimal ints.
    """
    hex_coordinates = [(hex_string[i:i + 2], hex_string[i + 2:i + 4])
                       for i in range(0, len(hex_string), 4)]
    dec_coordinates = [(int(x, 16), int(y, 16)) for (x, y) in hex_coordinates]
    return dec_coordinates


def coordinates_to_triangles(coordinates):
    """Convert coordinate list to triangle coordinate lists.

    Mechanism: Three consecutive tuples represent one triangle.
    Example: [(a, b), (c, d), (e, f), (g, h)]
        -> [[(a, b), (c, d), (e, f)], [(c, d), (e, f), (g, h)]]
    """
    return [coordinates[i:i + 3] for i in range(0, len(coordinates) - 2)]


def hex_to_triangles(hex_string):
    """Convert hex string to triangle coordinates."""
    assert not len(hex_string) % 4, "Invalid length - must be multiple of 4."
    coordinates = hex_to_coordinates(hex_string)
    return coordinates_to_triangles(coordinates)


def calculate_color(hex_string):
    """Convert hex color string to RGB tuple."""
    assert len(hex_string) == 3, "Invalid length."
    return tuple((255, 1, 3))


def extract_data(hex_hash):
    """Extract coordinates, color and bg information from name hash.

    coordinates: first 36 characters
    color: 36-39
    bg: last character (39)
    """
    return {"COORDS": hex_to_triangles(hex_hash[:36]),
            "COLOR": calculate_color(hex_hash[36:39]),
            "BG": int(hex_hash[-1], 16)}


def draw_avatar(data_dict):
    from PIL import Image, ImageDraw
    img_size = [256] * 2
    img = Image.new("RGB", img_size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(img, "RGBA")
    for triangle in data_dict["COORDS"]:
        draw.polygon(triangle, fill=(255, 255, 255, 15))
    img.show()


if __name__ == "__main__":
    name_hash = sha1_hash("mailea")
    data = extract_data(name_hash)
    draw_avatar(data)
