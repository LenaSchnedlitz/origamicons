from hashlib import sha1

username = "mailea"

sha = sha1()
sha.update(str.encode(username))

length = 160  # sha1 length * bits per hex number = 40 * 4

code = str(bin(int(sha.hexdigest(), 16))[2:].zfill(length))
code = [code[i:i + 4] for i in range(0, length - 2)]


def generator():
    distances = [2] * 22 + [3] * 38
    i = 0
    while distances:
        yield i
        i += distances.pop()


gen = generator()
formatted_code_parts = [code[i] for i in gen]
print(formatted_code_parts)
