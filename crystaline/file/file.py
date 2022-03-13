import json
from ..block import helper as hp


class File:
    PARAM_NAME, PARAM_CONTENT, PARAM_CREATOR, PARAM_CREATION_TXO = \
        '_name', '_content', '_creator', '_creation_transaction'

    def __init__(self, content, name, creator=None, creation_transaction=None):
        self._content = content
        self._name = name
        self._creator = creator
        self._creation_transaction = creation_transaction
        self._file_hash = self.get_hash()

    @property
    def name(self):
        return self._name

    @property
    def content(self):
        return self._content

    @property
    def creator(self):
        return self._creator

    @property
    def creation_transaction(self):
        return self._creation_transaction

    @property
    def file_hash(self):
        return self._file_hash

    def to_dict(self):
        return self.__dict__

    @classmethod
    def from_dict(cls, dict_in):
        return cls(dict_in[cls.PARAM_CONTENT], dict_in[cls.PARAM_NAME],
                   dict_in[cls.PARAM_CREATOR], dict_in[cls.PARAM_CREATION_TXO])

    def to_json(self):
        return json.dumps(self.__dict__)

    def get_hash(self):
        return hp.gen_hash(self.to_json())

    @staticmethod
    def from_json(file_json):
        return json.loads(file_json, object_hook=lambda obj:
        File(obj['_content'], obj['_name'],
             obj['_creator'], obj['_creation_transaction']))

    def __eq__(self, other):
        if isinstance(self, other.__class__):
            return other.content == self.content and other._name == self._name \
                   and other._creator == self._creator and other._creation_transaction == self._creation_transaction \
                   and other._file_hash == self._file_hash
        return False

