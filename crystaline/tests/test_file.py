import pytest
import json
from copy import deepcopy

from ..file.file import File

F_NAME = 'f_name'
F_CONTENT = 'f_content'
F_CREATOR = 'f_creator'
F_CREATION_TXO = 'f_creation_txo'

@pytest.fixture
def mfile():
    cls_dict = {
        File.PARAM_NAME: F_NAME,
        File.PARAM_CONTENT: F_CONTENT,
        File.PARAM_CREATOR: F_CREATOR,
        File.PARAM_CREATION_TXO: F_CREATION_TXO,
    }
    return File.from_dict(cls_dict)

def test_file_properties(mfile: File):
    assert mfile.name == F_NAME and \
           mfile.content == F_CONTENT and \
           mfile.creator == F_CREATOR and \
           mfile.creation_transaction == F_CREATION_TXO

def test_file_json(mfile: File):
    f_dict = json.loads(mfile.to_json())
    assert f_dict[File.PARAM_NAME] == F_NAME and \
           f_dict[File.PARAM_CONTENT] == F_CONTENT and \
           f_dict[File.PARAM_CREATOR] == F_CREATOR and \
           f_dict[File.PARAM_CREATION_TXO] == F_CREATION_TXO
def test_files_equality(mfile):
    assert mfile == deepcopy(mfile)