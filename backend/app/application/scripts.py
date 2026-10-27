from app.application.exceptions import InvalidURLError

from url_normalize import url_normalize, url_humanize
from urllib.parse import urlparse, parse_qs

import hashlib

def normalize_url(url: str) -> str:
    return url_humanize(
        url_normalize(url, default_scheme="http"), 
        ).split("#")[0]

def get_video_id(url: str) -> str:
    try:
        return parse_qs(urlparse(url).query)["v"][0]
    except (KeyError, IndexError):
        raise InvalidURLError("Wrong url")

def file_content_hash(
    data: bytes,
    algorithm: str = "sha256",
) -> str:
    h = hashlib.new(algorithm)
    h.update(data)
    return h.hexdigest()

def extract_file_extension(filename: str):
    return filename.split(".")[-1].lower()