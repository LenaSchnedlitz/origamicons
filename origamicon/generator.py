"""Generate a 250x250-avatar from a name string."""

RESIZE_FACTOR = 4  # high values make result images smoother
ALPHA = 50  # alpha value of triangles
BG_DARKNESS = 60  # will be subtracted from (r,g,b)-values of background
HUE_REDUCTION = 20  # gradient strength


def __sha1_hash(name):
    """Return SHA-1 hash of passed username.
    
    Attributes:
        name (str): any string, preferably a username
    """
    from hashlib import sha1
    sha = sha1()
    sha.update(str.encode(name))
    return sha.hexdigest()


def __to_coordinates(string):
    """Convert string into (x, y) - coordinate tuples.

    Two characters represent one value -> 4 characters per (x, y) tuple.
    Example: 01234567 -> [(01,23), (45,67)]
    
    Attributes:
        string (str): string of a number in any numeral system,
                      length must be divisible by 4
    """
    assert not len(string) % 4, "Invalid length - must be multiple of 4."
    return [(string[i:i + 2], string[i + 2:i + 4])
            for i in range(0, len(string), 4)]


def __to_decimal(hex_coordinates):
    """Convert hex 2d-coordinates into decimal coordinates.
    
    Attributes:
        hex_coordinates: collection of hexadecimal (x,y) coordinate tuples
    """
    return [(int(x, 16), int(y, 16)) for (x, y) in hex_coordinates]


def __rescale(coordinates):
    """Multiply coordinates with RESIZE_FACTOR
    
    Attributes:
        coordinates: collection of (x,y) coordinate tuples
    """
    return [(x * RESIZE_FACTOR, y * RESIZE_FACTOR) for (x, y) in coordinates]


def __to_triangles(coordinates):
    """Convert coordinate list into triangle (vertex) lists.

    Mechanism: Three consecutive tuples represent one triangle.
    Example: [(a, b), (c, d), (e, f), (g, h)]
        -> [[(a, b), (c, d), (e, f)], [(c, d), (e, f), (g, h)]]
    
    Attributes:
        coordinates: collection of (x,y) coordinate tuples
    """
    assert len(coordinates) >= 3, "Must contain at least 3 vertices."
    return [coordinates[i:i + 3] for i in range(0, len(coordinates) - 2)]


def __to_background_color(color):
    """Reduce (r,g,b) values by constant.
    
    Attributes:
        color: (r,g,b) tuple
    """
    return tuple([value - BG_DARKNESS for value in color])


def __change_hue(color, hue):
    """Reduce r, g or b by constant. Hue decides which value is reduced.
    
    Attributes:
        color: (r,g,b) or (r,g,b,a) tuple
        hue (int): index of hue that will be reduced; should be in range (0,4)
    """
    if hue >= 3:
        return color
    else:
        new_color = list(color)
        new_color[hue] -= HUE_REDUCTION
        return tuple(new_color)


def __extract_coordinates(hex_string):
    """Convert hex string into triangle coordinates.
    
    Attributes:
        hex_string (str): string only containing hexadecimal digits
    """
    coordinates = __to_coordinates(hex_string)
    coordinates = __to_decimal(coordinates)
    coordinates = __rescale(coordinates)
    coordinates = __to_triangles(coordinates)
    return coordinates


def __extract_color(hex_string):
    """Convert hex color string into (r,g,b) tuple.

    Result (r,g,b) values are in range 125-200 each.
    
    Attributes:
        hex_string (str): string of 3 hexadecimal digits.
    """
    assert len(hex_string) == 3, "Invalid length."
    return tuple(125 + 5 * int(digit, 16) for digit in hex_string)


def __extract_gradient(color, hex_digit):
    """Calculate two bg gradient colors. Hex_digit sets gradient hues.
    
    Attributes:
        color: (r,g,b,a) tuple
        hex_digit: any hex digit
    """
    bg_color = __to_background_color(color)
    number = int(hex_digit, 16)
    center = number // 4
    corner = number % 4
    return [__change_hue(bg_color, center), __change_hue(bg_color, corner)]


def __extract_data(sha_hex_hash):
    """Extract coordinates, color and bg information from name hash.

    coordinates: first 36 characters
    color: [36,39[
    background gradient hues: last character
    
    Attributes:
        sha_hex_hash (str): string consisting of 40 hexadecimal digits
    """
    coordinates = __extract_coordinates(sha_hex_hash[:36])
    color = __extract_color(sha_hex_hash[36:39])
    background_colors = __extract_gradient(color, sha_hex_hash[-1])
    return {"COORDS": coordinates, "COLOR": color, "BG": background_colors}


def __crop(square_img, new_size):
    """Crop a square image to new size.
    
    Attributes:
        square_img: PIL image, must have square shape
        new_size (int): desired length
    """
    old_size = square_img.size[0]
    correction = (old_size - new_size) % 2  # correct position for odd margins
    margin = (old_size - new_size - correction) // 2
    box = [margin] * 2 + [old_size - margin - correction] * 2
    return square_img.crop(box)


def __draw_gradient(img, center_color, corner_color):
    """Draw round gradient. Taken from http://stackoverflow.com/a/30669765
    
    Attributes:
        img: PIL image
        center_color: (r,g,b) or (r,g,b,a) tuple
        corner_color: (r,g,b) or (r,g,b,a) tuple
    """
    import math as math
    size = img.size[0]

    for y in range(img.size[1]):
        for x in range(size):
            # Find the distance to the center_color
            distance = math.sqrt((x - size / 2) ** 2 + (y - size / 2) ** 2)

            # Make it on a scale from 0 to 1
            distance = float(distance) / (math.sqrt(2) * size / 2)

            # Calculate r, g, and b values
            r = corner_color[0] * distance + center_color[0] * (1 - distance)
            g = corner_color[1] * distance + center_color[1] * (1 - distance)
            b = corner_color[2] * distance + center_color[2] * (1 - distance)

            # Place the pixel
            img.putpixel((x, y), (int(r), int(g), int(b)))
    return img


def __draw_avatar(data_dict):
    """Draw an avatar from given data.
    
    Attributes:
        data_dict: must be formatted like results of __extract_data
    """
    from PIL import Image, ImageDraw
    size = 256
    color = data_dict["COLOR"] + (ALPHA,)
    center_color, corner_color = data_dict["BG"]
    triangles = data_dict["COORDS"]

    img = Image.new("RGB", [size] * 2, (120, 120, 150))
    img = __draw_gradient(img, center_color, corner_color)

    # resize to make edges smoother
    img = img.resize([size * RESIZE_FACTOR] * 2, Image.ANTIALIAS)
    draw = ImageDraw.Draw(img, "RGBA")

    for triangle in triangles:
        draw.polygon(triangle, fill=color, outline=color)

    # return to original size
    img = img.resize([size] * 2, Image.ANTIALIAS)
    img = __crop(img, 250)
    return img


def get_image(name):
    """Get image for passed name.
    
    Attributes:
        name (str): any string, preferably a username
    """
    name_hash = __sha1_hash(name)
    data = __extract_data(name_hash)
    avatar = __draw_avatar(data)
    return avatar


if __name__ == "__main__":
    username = input("What's your name? \n>")
    get_image(username)
