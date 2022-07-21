import pytest
from pathlib import Path
import random
import os
import time
import string
from copy import deepcopy

from crystaline.block.block import Block, BLOCK_FILE_SIZE
from crystaline.block import helper
from crystaline.transaction.transaction import Transaction
from crystaline.file.file import File

B_VERSION, B_PREV_HASH, B_DIFF_TARGET, B_NONCE, B_FILES, B_TRANSACTIONS, = (
    "version",
    "prev_hash",
    random.randint(1, 1000),
    random.randint(1, 1000),
    [File("fcontent", "fname")],
    [Transaction("1", "2"), Transaction("3", "4")],
)

TMP_FILE_NAME = "tmp_file"


@pytest.fixture()
def mblock():
    return Block(
        B_VERSION,
        B_PREV_HASH,
        B_DIFF_TARGET,
        B_NONCE,
        transactions=B_TRANSACTIONS,
        files=B_FILES,
    )


@pytest.fixture()
def tmp_file(tmp_path):
    file_path = os.path.join(tmp_path, TMP_FILE_NAME)
    with open(file_path, "w") as fp:
        fp.write(str(random.random() * 1000))
    return file_path


@pytest.fixture(
    params=[
        {"total_size": i, "n_files": j, "exp_out": k}
        for i, j, k in [
            (BLOCK_FILE_SIZE - 8, 1, False),
            (BLOCK_FILE_SIZE - 12, 4, True),
            (BLOCK_FILE_SIZE + 8, 8, False),
            (BLOCK_FILE_SIZE - 24, 8, True),
        ]
    ]
)
def tmp_files(tmp_path, request):
    total_size, n_files, expected_output = (
        request.param["total_size"],
        request.param["n_files"],
        request.param["exp_out"],
    )
    assert total_size % n_files == 0, "Total_size is not divisible by n_files."
    f_size = total_size // n_files

    files = []
    for i in range(n_files):
        file_path = os.path.join(tmp_path, TMP_FILE_NAME + str(i))
        files.append(file_path)
        with open(file_path, "wb") as fp:
            random_content = "".join(
                random.choice(string.ascii_lowercase + string.digits)
                for _ in range(f_size)
            )
            fp.write(random_content.encode())
    return files, expected_output


def test_block_params(mblock: Block):
    assert (
        mblock.version == B_VERSION
        and mblock.prev_hash == B_PREV_HASH
        and mblock.difficulty_target == B_DIFF_TARGET
        and mblock.nonce == B_NONCE
        and mblock.transactions == B_TRANSACTIONS
        and mblock.files == B_FILES
    )


def test_block_timestamp_is_early_enough(mblock: Block):
    assert mblock.timestamp <= time.time()


def test_block_to_dict(mblock: Block):
    assert (
        mblock.version == B_VERSION
        and mblock.prev_hash == B_PREV_HASH
        and mblock.difficulty_target == B_DIFF_TARGET
        and mblock.nonce == B_NONCE
        and mblock.files == B_FILES
        and mblock.transactions == B_TRANSACTIONS
    )


def test_upload_file(mblock: Block, tmp_file: str):
    mblock.upload_file(tmp_file)

    with open(tmp_file, "rb") as fp:
        assert mblock._files[-1] == File(fp.read(), Path(tmp_file).name)


def test_upload_and_download_file(mblock: Block, tmp_file: str, tmp_path: str):
    mblock.upload_file(tmp_file)

    download_dir = os.path.join(tmp_path, "down_dir")
    if not os.path.exists(download_dir):
        os.mkdir(download_dir)

    mblock.download_file(download_dir, -1)

    with open(os.path.join(download_dir, TMP_FILE_NAME), "rb") as fp:
        assert mblock._files[-1] == File(fp.read(), Path(tmp_file).name)


@pytest.mark.skip
def test_is_files_size_valid(mblock: Block, tmp_files: list):
    files, expected_output = tmp_files
    for fp in files:
        mblock.upload_file(fp)
    assert mblock.is_files_size_valid() == expected_output


@pytest.mark.skip
def test_is_valid1(tmp_files):
    files, is_files_size_valid = tmp_files
    version = None if random.randint(0, 1) == 0 else B_VERSION
    prev_hash = None if random.randint(0, 1) == 0 else B_PREV_HASH
    difficulty_target = None if random.randint(0, 1) == 0 else B_DIFF_TARGET
    nonce = None if random.randint(0, 1) == 0 else B_NONCE
    block = Block(
        version,
        prev_hash,
        difficulty_target,
        nonce,
        transactions=B_TRANSACTIONS,
        files=[],
    )

    for fp in files:
        block.upload_file(fp)

    expected_out = (
        is_files_size_valid
        and (version is not None)
        and (prev_hash is not None)
        and (difficulty_target is not None)
        and (nonce is not None)
    )
    assert block.is_valid() == expected_out


@pytest.mark.skip
def test_is_valid2(tmp_files):
    files, is_files_size_valid = tmp_files
    version = None if random.randint(0, 1) == 0 else B_VERSION
    prev_hash = None if random.randint(0, 1) == 0 else B_PREV_HASH
    difficulty_target = None if random.randint(0, 1) == 0 else B_DIFF_TARGET
    nonce = None if random.randint(0, 1) == 0 else B_NONCE
    block = Block(
        version,
        prev_hash,
        difficulty_target,
        nonce,
        transactions=B_TRANSACTIONS,
        files=[],
    )

    for fp in files:
        block.upload_file(fp)

    expected_out = (
        is_files_size_valid
        and (version is not None)
        and (prev_hash is not None)
        and (difficulty_target is not None)
        and (nonce is not None)
    )
    assert block.is_valid() == expected_out


def test_save_and_load_block(mblock: Block, tmp_path: str):
    f_path = mblock.save(tmp_path)
    block = Block.load(f_path)

    assert mblock == block


def test_get_files_hash(mblock: Block):
    files = mblock.files
    expected_hash = ""
    for f in files:
        expected_hash += f.hash
    expected_hash = helper.gen_hash(expected_hash)

    assert mblock.get_files_hash() == expected_hash


def test_get_transactions_hash(mblock: Block):
    transactions = mblock.transactions
    expected_hash = ""
    for transaction in transactions:
        expected_hash += transaction.get_hash()
    expected_hash = helper.gen_hash(expected_hash)

    assert mblock.get_transactions_hash() == expected_hash


def test_blocks_equality(mblock):
    assert mblock == deepcopy(mblock)
