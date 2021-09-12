import pytest
from crystaline.block.Block import Block
import time


@pytest.fixture
def mblock():
    return Block('version', 'prev_hash', 1000, 999)


def test_block_params(mblock):
    assert mblock.version == 'version' and mblock.prev_hash == 'prev_hash' and mblock.difficulty_target == 1000 and mblock.nonce == 999


def test_block_timestamp_is_early_enough(mblock):
    print(mblock.timestamp)
    assert mblock.timestamp <= time.time()


def test_block_timestamp_is_exact(mblock):
    print(mblock.timestamp)
    assert mblock.timestamp == int(time.time())
