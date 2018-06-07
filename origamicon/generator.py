"""Generate a 250x250px avatar from a name string."""

from PIL import Image, ImageDraw

import math as math

ORIGAMICON_SIZE = 250  # size of the final result
PROCESSING_SIZE = 16 ** 2  # size used during origamicon creation
RESIZE_FACTOR = 4  # high values make result images smoother


def __sha1_hash(name):
    from hashlib import sha1
    sha = sha1()
    sha.update(str.encode(name))
    return sha.hexdigest()


def to_decimal(hex_string):
    return int(hex_string, 16)


def scale_up(number):
    return number * RESIZE_FACTOR


# COORDINATES #################################################################

def to_coordinates(hex_string):
    def substrings(string):
        return (string[i:i + 2] for i in range(0, len(string), 2))

    def pairs(items):
        return (tuple([item, next(items)]) for item in items)

    parts = substrings(hex_string)
    return pairs(scale_up(to_decimal(part)) for part in parts)


def triangles(coords):
    a = next(coords)
    b = next(coords)
    c = next(coords)

    while c is not None:
        yield tuple([a, b, c])
        try:
            a, b, c = b, c, next(coords)
        except StopIteration:
            c = None


# COLORS ######################################################################

def colors(string):
    def saturate(color, position, base):
        amount = 10 * base + base ** 2
        if position == 3:
            for index in range(3):
                color[index] += amount // 3
        else:
            color[position] += amount
        return color

    def fade(color, position, base):
        amount = max(base, 0) ** 2
        if position == 3:
            color[position] -= amount
        else:
            color[position] -= amount
        return color

    base_color_data = string[:3]
    r, g, b = [to_decimal(char) * 4 + 55 for char in base_color_data]
    alpha = 255

    gradient_data = to_decimal(string[-1])
    pos1, pos2 = gradient_data % 4, gradient_data // 4

    for i in range(1, 8):
        yield tuple(
            fade(
                saturate([r, g, b, alpha], pos1, i),
                pos2, max(5 - i, 0))
        )


# IMAGE #######################################################################

def new_image():
    img = Image.new('RGB', [PROCESSING_SIZE] * 2, (0, 0, 0))

    for y in range(PROCESSING_SIZE):
        for x in range(PROCESSING_SIZE):
            # Find distance from center_color
            distance = math.sqrt(
                (x - PROCESSING_SIZE / 2) ** 2 +
                (y - PROCESSING_SIZE / 2) ** 2
            )
            # Use scale from 0 to 1
            distance = distance / (math.sqrt(2) * PROCESSING_SIZE / 2)

            # Calculate value
            value = int(235 * distance + 255 * (1 - distance))

            # Place the pixel
            img.putpixel((x, y), tuple([value] * 3))

    # Resize to make edges smoother
    img = img.resize([scale_up(PROCESSING_SIZE)] * 2, Image.ANTIALIAS)
    return img


def post_process(img):
    img = img.resize([PROCESSING_SIZE] * 2, Image.ANTIALIAS)

    size_difference = PROCESSING_SIZE - ORIGAMICON_SIZE
    correction = size_difference % 2  # correct position for odd margins
    margin = (size_difference - correction) // 2
    box = [margin] * 2 + [PROCESSING_SIZE - margin - correction] * 2
    return img.crop(box)


def origamicon(triangle_data, color_data):
    img = new_image()

    draw = ImageDraw.Draw(img, 'RGBA')

    for triangle in triangle_data:
        color = next(color_data)
        draw.polygon(triangle, fill=color, outline=color)

    return post_process(img)


# CALL ########################################################################

def create_origamicon(name):
    """Create the origamicon for the given name

    :param name: a string (username)
    :return: the created origamicon
    """
    name_hash = __sha1_hash(name)
    triangle_data = triangles(to_coordinates(name_hash[:36]))
    color_data = colors(name_hash[36:])

    return origamicon(triangle_data, color_data)


if __name__ == '__main__':
    username = input("What's your name? \n>")
    origamicon = create_origamicon(username)
    origamicon.format = 'PNG'
    origamicon.show()
