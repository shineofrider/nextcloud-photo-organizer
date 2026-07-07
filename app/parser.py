import xml.etree.ElementTree as ET
from pathlib import PurePosixPath

from models import WebDAVItem

NS = {
    "d": "DAV:"
}


def parse_propfind(
    xml: str,
    webdav_root: str,
) -> list[WebDAVItem]:
    root = ET.fromstring(xml)

    items = []

    for response in root:

        href = response.find("d:href", NS)

        full_path = href.text

        relative_path = full_path.replace(
          webdav_root,
          ""
        )

        path = PurePosixPath(relative_path)

        print(path)
        print(path.name)

    return items
