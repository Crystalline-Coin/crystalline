import json

class File:

    def __init__(self, content, name, creator = None, creation_transaction = None):
        self._content = content
        self._name = name
        self._creator = creator
        self._creation_transaction = creation_transaction

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

    def to_dict(self):
        return self.__dict__

    @staticmethod
    def from_dict(dict):
        return File(dict['_content'], dict['_name'],
                    dict['_creator'], dict['_creation_transaction'])

    def to_json(self):
        return json.dumps(self.__dict__)

    @staticmethod
    def from_json(file_json):
        return json.loads(file_json, object_hook = lambda obj: 
                                    File(obj['_content'], obj['_name'],
                                    obj['_creator'], obj['_creation_transaction']))
                                    