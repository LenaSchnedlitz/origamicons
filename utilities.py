def hex_to_bin(hex_string):
    """Convert hex to binary string."""
    length = 160  # hash length * bits per hex number
    return str(bin(int(hex_string, 16))[2:].zfill(length))


def hex_to_rgb(hex_string):
    """Convert hex string to rgb tuple"""
    parts = (hex_string[i: i + 2] for i in range(0, len(hex_string), 2))
    return [int(part, 16) for part in parts]
