from typing import List
import json


def read_urls(path: str) -> List[str]:
    with open(path) as f:
        lines = [like["string_list_data"] for like in json.load(f)["likes_media_likes"]]
        urls = [item[0]["href"] for item in lines]
        return urls
