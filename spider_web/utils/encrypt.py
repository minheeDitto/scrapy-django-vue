import hashlib


def get_encrpt(filename):
    secret = hashlib.sha256()
    secret.update(filename.encode())
    final = secret.hexdigest()[:21]
    return final


