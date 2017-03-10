from hashlib import sha1

username = "mailea"

sha = sha1()
sha.update(str.encode(username))
print(sha.hexdigest())
