def hex_to_bin(sha_hash):
    """Convert SHA-1 hash to binary and return result as a string."""
    length = 160  # hash length * bits per hex number
    return str(bin(int(sha_hash, 16))[2:].zfill(length))


def sha1_hash(username):
    """Return (hexadecimal) SHA-1 hash of passed username."""
    from hashlib import sha1
    sha = sha1()
    sha.update(str.encode(username))
    return hex_to_bin(sha.hexdigest())


def split_position():
    """Arbitrary algorithm"""
    distances = [2] * 22 + [3] * 38
    i = 0
    while distances:
        yield i
        i += distances.pop()


def split_for_drawing(bin_hash):
    """Split binary (str) hash into 61 parts of length 4."""
    parts = [bin_hash[i:i + 4] for i in range(0, len(bin_hash) - 2)]
    indices = split_position()
    return [parts[i] for i in indices]


name_hash = sha1_hash("mailea")
hash_parts = split_for_drawing(name_hash)


print(hash_parts)
