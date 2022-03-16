from file import File

if __name__ == "__main__":
    json_str = {
        "_content": "Hi",
        "_name": "Hello",
        "_creator": "taha",
        "_creation_transaction": 0,
    }
    new_file = File.from_dict(json_str)
    print(new_file.name)
    print(new_file.content)
    print(new_file.to_dict())
