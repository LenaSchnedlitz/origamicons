def hex_to_bin(sha_hash):
    length = 160  # hash length * bits per hex number
    bin_string = str(bin(int(sha_hash, 16))[2:].zfill(length))
    return [bin_string[i:i + 4] for i in range(0, length - 2)]


def sha1_hash(username):
    from hashlib import sha1
    sha = sha1()
    sha.update(str.encode(username))
    return hex_to_bin(sha.hexdigest())


def split_position():
    distances = [2] * 22 + [3] * 38
    i = 0
    while distances:
        yield i
        i += distances.pop()


def split_for_drawing(bin_hash):
    indices = split_position()
    return [bin_hash[i] for i in indices]


name_hash = sha1_hash("mailea")
hash_parts = split_for_drawing(name_hash)


print(hash_parts)
