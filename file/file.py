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

    def to_json(self):
        file = {
            'content' : self._content,
            'name' : self._name,
            'creator' : self._creator,
            'creation_transaction' : self._creation_transaction
        }
        return json.dumps(file)

    @staticmethod
    def from_json(self, file_json):
        file = json.loads(file_json)
        return File(file['content'],
                    file['name'],
                    file['creator'],
                    file['creation_transaction'])

