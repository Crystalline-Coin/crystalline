import math
from hashlib import sha3_256, sha384

REWARD_INTERV = 250000
INITIAL_REWARD_R = 50


def gen_hash(data: str):
    data_arr = bytearray(data, encoding="utf-8")
    return sha384(sha3_256(data_arr).digest()).hexdigest()


def gen_hash_encoded(data: bytearray):
    return sha384(sha3_256(data).digest()).hexdigest()


def __calc_block_reward_R_i(R: int, i: int):
    return R / (2 ** (i - 1))


def __calc_block_reward_i(block_height: int, reward_interval: int):
    return math.ceil(block_height / reward_interval)


def __calc_reward(block_height: int, R_i: float, reward_interval: int, i: int):
    return math.pow(
        (1 + R_i), (block_height - reward_interval * i) / (1.0 * reward_interval)
    ) - math.pow(
        (1 + R_i), (block_height - 1 - reward_interval * i) / (1.0 * reward_interval)
    )


def get_block_reward(block_height: int):
    i = __calc_block_reward_i(block_height, REWARD_INTERV)
    R_i = __calc_block_reward_R_i(INITIAL_REWARD_R, i)
    return __calc_reward(block_height, R_i, REWARD_INTERV, i)
