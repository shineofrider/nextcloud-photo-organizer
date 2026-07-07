from dataclasses import dataclass
from datetime import datetime
from enum import Enum, auto

class SyncDecision(Enum):
    MOVE = auto()
    DELETE_DUPLICATE = auto()
    CONFLICT = auto()

@dataclass
class WebDAVItem:
    name: str
    path: str
    is_dir: bool

    size: int | None = None
    last_modified: str | None = None
    etag: str | None = None

@dataclass
class MoveOperation:
    source: WebDAVItem
    destination_path: str
    decision: SyncDecision | None = None
