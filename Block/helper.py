from hashlib import sha3_256, sha384


def gen_hash(data: str):
    data_arr = bytearray(data, encoding='utf-8')
    return sha384(sha3_256(data_arr).digest()).hexdigest()


def gen_hash_encoded(data: bytearray):
    return sha384(sha3_256(data).digest()).hexdigest()
