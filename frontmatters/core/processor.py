import codecs
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .default_handlers import BaseHandler

from frontmatter.util import u
from frontmatter.default_handlers import YAMLHandler, JSONHandler, TOMLHandler


# global handlers
handlers = [
    Handler()
    for Handler in [YAMLHandler, JSONHandler, TOMLHandler]
    if Handler is not None
]


def detect_format(text: str, handlers):
    """
    Figure out which handler to use, based on metadata.
    Returns a handler instance or None.
    """
    for handler in handlers:
        if handler.detect(text):
            return handler
    return None


def parse(text: str, encoding: str = "utf-8", handler=None, **defaults):
    """
    Parse text with frontmatter, return metadata and content.
    """
    # ensure unicode first
    text = u(text, encoding).strip()

    # metadata starts with defaults
    metadata = defaults.copy()

    # this will only run if a handler hasn't been set higher up
    handler = handler or detect_format(text, handlers)
    if handler is None:
        return metadata, text

    # split on the delimiters
    try:
        fm, content = handler.split(text)
    except ValueError:
        # if we can't split, bail
        return metadata, text

    # parse, now that we have frontmatter
    fm_data = handler.load(fm)
    if isinstance(fm_data, dict):
        metadata.update(fm_data)

    return metadata, content.strip()


def loads(text: str, encoding: str = "utf-8", handler=None, **defaults):
    """
    Parse text and return a Post.
    """
    text = u(text, encoding)
    handler = handler or detect_format(text, handlers)
    metadata, content = parse(text, encoding, handler, **defaults)
    return Post(content, handler, **metadata)


def dumps(post, handler=None, **kwargs):
    """
    Serialize a Post to a string and return text.
    """
    if handler is None:
        handler = getattr(post, "handler", None) or YAMLHandler()

    return handler.format(post, **kwargs)


class Post(object):
    """
    A post contains content and metadata from Front Matter.
    """

    def __init__(self, content: str, handler=None, **metadata):
        self.content = str(content)
        self.metadata = metadata
        self.handler = handler

    def __getitem__(self, name: str):
        "Get metadata key"
        return self.metadata[name]

    def __contains__(self, item):
        "Check metadata contains key"
        return item in self.metadata

    def __setitem__(self, name: str, value):
        "Set a metadata key"
        self.metadata[name] = value

    def __delitem__(self, name: str):
        "Delete a metadata key"
        del self.metadata[name]

    def __str__(self):
        return self.content

    def get(self, key: str, default=None):
        "Get a key, fallback to default"
        return self.metadata.get(key, default)

    def keys(self):
        "Return metadata keys"
        return self.metadata.keys()

    def values(self):
        "Return metadata values"
        return self.metadata.values()


class FrontmatterProcessor:
    def __init__(self, filepath: Path):
        self.filepath = filepath
        self.post = self._load_post()

    def _load_post(self):
        with open(self.filepath, "r", encoding="utf-8") as f:
            return loads(f.read())

    def has_frontmatter(self, key: str) -> bool:
        return key in self.post.metadata

    def update_frontmatter(self, key: str, value: str):
        self.post.metadata[key] = value
        self._write_post()

    def _write_post(self):
        with open(self.filepath, "w", encoding="utf-8") as f:
            f.write(dumps(self.post))

    @property
    def content(self):
        return self.post.content