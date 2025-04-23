import base64

import orjson


def encode_dict_to_base64(data: dict) -> str:
    return base64.b64encode(orjson.dumps(data)).decode("utf-8")


def decode_dict_to_base64(encoded_data: str) -> dict:
    return orjson.loads(base64.b64decode(encoded_data.encode("utf-8")))


def enconde_dict_to_str(data: dict) -> str:
    return orjson.dumps(data).decode("utf-8")
