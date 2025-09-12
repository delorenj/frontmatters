import frontmatter
from pathlib import Path

class FrontmatterProcessor:
    def __init__(self, filepath: Path):
        self.filepath = filepath
        self.post = self._load_post()

    def _load_post(self):
        with open(self.filepath, "r", encoding="utf-8") as f:
            return frontmatter.loads(f.read())

    def has_frontmatter(self, key: str) -> bool:
        return key in self.post.metadata

    def update_frontmatter(self, key: str, value: str):
        self.post.metadata[key] = value
        self._write_post()

    def _write_post(self):
        with open(self.filepath, "w", encoding="utf-8") as f:
            f.write(frontmatter.dumps(self.post))

    @property
    def content(self):
        return self.post.content