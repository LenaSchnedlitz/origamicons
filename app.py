DOTS = 61  # number of drawn 'dots' in image


def sha1_hash(username):
    """Return SHA-1 hash of passed username as string of zeros and ones."""

    def hex_to_bin(sha_hash):
        """Convert SHA-1 (hex) hash to binary number string."""
        length = 160  # hash length * bits per hex number
        return str(bin(int(sha_hash, 16))[2:].zfill(length))

    from hashlib import sha1
    sha = sha1()
    sha.update(str.encode(username))
    return hex_to_bin(sha.hexdigest())


def split(string, position):
    """Split string at given position, return both parts."""
    return string[:position], string[position:]


def get_dot_indices(margin=8, size=250):
    """Create tuples that 'draw' a circle."""
    shape = ((0, 0, 0, 1, 1, 1, 0, 0, 0),
             (0, 1, 1, 1, 1, 1, 1, 1, 0),
             (0, 1, 1, 1, 1, 1, 1, 1, 0),
             (1, 1, 1, 1, 1, 1, 1, 1, 1),
             (1, 1, 1, 1, 1, 1, 1, 1, 1),
             (1, 1, 1, 1, 1, 1, 1, 1, 1),
             (0, 1, 1, 1, 1, 1, 1, 1, 0),
             (0, 1, 1, 1, 1, 1, 1, 1, 0),
             (0, 0, 0, 1, 1, 1, 0, 0, 0))

    distance = (size - 2 * margin) // len(shape)
    coords = [margin + distance // 2 + i * distance for i in range(len(shape))]

    tuples = []
    for i, row in enumerate(shape):
        for j, cell in enumerate(row):
            if cell:
                tuples.append((coords[i], coords[j]))

    return tuples


def draw_dots(hash_parts):
    from PIL import Image, ImageDraw
    img = Image.new('RGBA', (250, 250), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    r = 9
    tuples = get_dot_indices()
    for i in range(len(tuples)):
        x, y = tuples[i]
        draw.ellipse((x - r, y - r, x + r, y + r),
                     fill=(255, 0, 0, 0))


name_hash = sha1_hash("mailea")
img_hash = name_hash * 2

dot_data, img_hash = split(img_hash, 5 * DOTS)
dot_data = [dot_data[i:i + 5] for i in range(0, len(dot_data), 5)]

palette, img_hash = split(img_hash, 5)
bg, img_hash = split(img_hash, 2)
shape, img_hash = split(img_hash, 2)

draw_dots(dot_data)

