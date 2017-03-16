def sha1_hash(username):
    """Return SHA-1 hash of passed username as string of zeros and ones."""
    from hashlib import sha1
    import utilities as u
    sha = sha1()
    sha.update(str.encode(username))
    hex_hash = sha.hexdigest()
    bin_hash = u.hex_to_bin(hex_hash)
    return bin_hash


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


if __name__ == "__main__":
    name_hash = sha1_hash("mailea")
    data = extract_data(name_hash)
    from drawing import draw_image

    draw_image(data)
