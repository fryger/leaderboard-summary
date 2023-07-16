import os
import json
import base64
import hashlib


def save_dict_to_file(data, file_path):
    with open(file_path, "w") as file:
        json.dump(data, file)


def load_dict_from_file(file_path):
    with open(file_path, "r") as file:
        return json.load(file)


def cache_request():
    def decorator(func):
        def wrapper():
            file_path = f"./tmp/{func.__name__}.json"

            if os.path.exists(file_path):
                data = load_dict_from_file(file_path)
            else:
                data = None

            if not data:
                data = func()
                save_dict_to_file(data, file_path)

            return data

        return wrapper

    return decorator


def create_hash(*args):
    concatenated_string = "".join(str(arg) for arg in args)
    hash = hashlib.shake_256()
    hash.update(concatenated_string.encode("utf-8"))
    hash_value = hash.hexdigest(7)

    return hash_value
