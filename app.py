RESIZE_FACTOR = 4  # high values make result images smoother


def sha1_hash(username):
    """Return SHA-1 hash of passed username."""
    from hashlib import sha1
    sha = sha1()
    sha.update(str.encode(username))
    return sha.hexdigest()


def hex_to_coordinates(hex_string):
    """Convert hex string to (x, y) - coordinate tuples.

    Two digits represent one value -> 4 digits per (x, y) tuple.
    After splitting, hex numbers are converted to decimals and multiplied by
    RESIZE_FACTOR.
    """
    hex_coordinates = [(hex_string[i:i + 2], hex_string[i + 2:i + 4])
                       for i in range(0, len(hex_string), 4)]
    dec_coordinates = [(int(x, 16) * RESIZE_FACTOR, int(y, 16) * RESIZE_FACTOR)
                       for (x, y) in hex_coordinates]
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
    """Convert hex color string to RGBA tuple.

    RGB-values are in range 125-200 each. A-value is 30.
    """
    assert len(hex_string) == 3, "Invalid length."
    rgb = tuple(125 + 5 * int(digit, 16) for digit in hex_string)
    return rgb + (50,)


def change_hue(color, how):
    """Change color tuple based on how-value."""
    assert how in range(4), "How must be an integer in range(0, 4)"
    if how == 3:
        return tuple([value - 60 for value in color])
    else:
        new = [value - 60 for value in color]
        new[how] -= 20
        return tuple(new)


def calculate_gradient(hex_number, color):
    """Use passed hex number to change color tuple in two different ways."""
    number = int(hex_number, 16)
    start = number // 4
    end = number % 4
    return [change_hue(color, start), change_hue(color, end)]


def extract_data(hex_hash):
    """Extract coordinates, color and bg information from name hash.

    coordinates: first 36 characters
    color: [36,39[
    bg: last character (in this case 39)
    """
    triangle_coords = hex_to_triangles(hex_hash[:36])
    color = calculate_color(hex_hash[36:39])
    background_colors = calculate_gradient(hex_hash[-1], color)
    return {"COORDS": triangle_coords, "COLOR": color, "BG": background_colors}


def crop_image(img, new_size):
    """Crop a square image to new size."""
    old_size = img.size[0]
    if (old_size - new_size) % 2:
        margin = (old_size - new_size - 1) // 2
        box = [margin] * 2 + [old_size - margin - 1] * 2
    else:
        margin = (old_size - new_size) // 2
        box = [margin] * 2 + [old_size - margin] * 2
    return img.crop(box)


def draw_gradient(img, colors):
    """Draw round gradient. Taken from http://stackoverflow.com/a/30669765"""
    import math as math
    center, corner = colors
    size = img.size[0]

    for y in range(img.size[1]):
        for x in range(size):
            # Find the distance to the center
            distance = math.sqrt((x - size / 2) ** 2 + (y - size / 2) ** 2)

            # Make it on a scale from 0 to 1
            distance = float(distance) / (math.sqrt(2) * size / 2)

            # Calculate r, g, and b values
            r = corner[0] * distance + center[0] * (1 - distance)
            g = corner[1] * distance + center[1] * (1 - distance)
            b = corner[2] * distance + center[2] * (1 - distance)

            # Place the pixel
            img.putpixel((x, y), (int(r), int(g), int(b)))
    return img


def draw_avatar(data_dict):
    from PIL import Image, ImageDraw
    size = 256
    color = data_dict["COLOR"]

    img = Image.new("RGB", [size] * 2, (120, 120, 150))
    img = draw_gradient(img, data_dict["BG"])

    # resize to make edges smoother
    img = img.resize([size * RESIZE_FACTOR] * 2, Image.ANTIALIAS)
    draw = ImageDraw.Draw(img, "RGBA")

    for triangle in data_dict["COORDS"]:
        draw.polygon(triangle, fill=color, outline=color)

    # return to original size
    img = img.resize([size] * 2, Image.ANTIALIAS)
    img = crop_image(img, 250)
    img.show()


if __name__ == "__main__":
    name_hash = sha1_hash("mailea")
    data = extract_data(name_hash)
    draw_avatar(data)
