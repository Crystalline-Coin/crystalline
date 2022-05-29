import json
from crystaline.block import helper as hp

PARAM_NAME, PARAM_CONTENT, PARAM_CREATOR, PARAM_CREATION_TXO = (
    "_name",
    "_content",
    "_creator",
    "_creation_transaction",
)


class File:
    def __init__(self, content, name, creator=None, creation_transaction=None):
        self._content = content

        self._name = name
        self._creator = creator
        self._creation_transaction = creation_transaction
        self._hash = self.get_hash()

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
    def hash(self):
        return self._hash

    def to_dict(self):
        return {
            PARAM_NAME: self._name,
            PARAM_CONTENT: str(self._content),
            PARAM_CREATOR: self._creator,
            PARAM_CREATION_TXO: self._creation_transaction,
        }

    @classmethod
    def from_dict(cls, dict_in):
        return cls(
            dict_in[PARAM_CONTENT],
            dict_in[PARAM_NAME],
            dict_in[PARAM_CREATOR],
            dict_in[PARAM_CREATION_TXO],
        )

    def get_size(self):
        return len(self.to_json())

    def to_json(self):
        return json.dumps(self.to_dict())

    def get_hash(self):
        return hp.gen_hash(self.to_json())

    @staticmethod
    def from_json(file_json):
        return json.loads(
            file_json,
            object_hook=lambda obj: File(
                obj[PARAM_CONTENT],
                obj[PARAM_NAME],
                obj[PARAM_CREATOR],
                obj[PARAM_CREATION_TXO],
            ),
        )

    def __eq__(self, other):
        if isinstance(self, other.__class__):
            return (
                other.content == self.content
                and other.name == self._name
                and other.creator == self._creator
                and other.creation_transaction == self._creation_transaction
                and other.hash == self._hash
            )
        return False
