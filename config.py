import json


class Config:
    firefox_profile_path: str
    liked_posts_path: str

    def __init__(self, config_path: str):
        with open(config_path) as f:
            lines = json.load(f)
            self.firefox_profile_path = lines["firefox_profile_path"]
            self.liked_posts_path = lines["liked_posts_path"]
