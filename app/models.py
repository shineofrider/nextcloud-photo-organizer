from dataclasses import dataclass
from datetime import datetime


@dataclass
class WebDAVItem:
    """
    path è sempre relativo alla root WebDAV configurata.
    Esempio: Foto/2025/IMG0001.jpg
    """

    name: str
    path: str
    is_dir: bool
    size: int | None = None
    modified: datetime | None = None