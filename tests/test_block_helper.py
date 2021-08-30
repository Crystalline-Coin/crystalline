import pytest
from crystaline.Block.helper import gen_hash_encoded, gen_hash


def test_block_hash_generation1():
    data_str = '18c05d189f44e7a5dd7124d6f4d3c9a9802bf7b647c1d5ae295d35e5be5d7772'
    exp_res = 'aea10f6c1dd2321e8c8bb5037efc45e2c01b2e55949c1718ab5e72cf82642c74cab04da15b319054fdfcab4f650a8765'
    assert gen_hash(data_str) == exp_res


def test_block_hash_generation2():
    data_str = '18c05d189f44e7a5dd7124d6f4d3c9a9802bf7b647c1d5ae295d35e5be5d7772'
    exp_res = 'aea10f6c1dd2321e8c8bb5037efc45r2c01b2e55949c1718ab5e72cf82642c74cab04da15b319054fdfcab4f650a8765'
    assert gen_hash(data_str) != exp_res


def test_block_hash_generation_encoded1():
    data_str = '18d7c272f74122eeeaa0316416c11809438d7e5f171146f3f618a1ecd321358678140cf97bc8ea759e13b75bfb00a272ebec8c75ae9c2048960693ad323662de'
    exp_res = '373de55a59c614bee9a08d430d8169e93663527505bebe786dbe7b521b578db446f5b66fc4c0ff01f66ff0ede839448f'
    assert gen_hash_encoded(bytearray(data_str, encoding='utf-8')) == exp_res


def test_block_hash_generation_encoded2():
    data_str = '18d7c272f74122eeeaa0316416c11809438d7e5f171146f3f618a1ecd321358678140cf97bc8ea759e13b75bfb00a272ebec8c75ae9c2048960693ad323662de'
    exp_res = '373de55a59c614bee9a08d430d8169e93663527505bebe786dbe7b521b578db446f5b66fc4c0ff01f66ff0ede839448e'
    assert gen_hash_encoded(bytearray(data_str, encoding='utf-8')) != exp_res
