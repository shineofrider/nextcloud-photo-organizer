import xml.etree.ElementTree as ET
from pathlib import PurePosixPath
from app.models import WebDAVItem
from urllib.parse import unquote

NS = {
    "d": "DAV:"
}


def parse_propfind(
    xml: str,
    webdav_root: str,
    current_path: str,
    
) -> list[WebDAVItem]:

    root = ET.fromstring(xml)

    items = []

    for response in root:

        href = response.find("d:href", NS)

        if href is None or href.text is None:
            continue

        full_path = unquote(href.text)

        prefix = f"{webdav_root}{current_path.strip('/')}/"

        relative_path = full_path.replace(
            prefix,
            ""
        ).rstrip("/")

        # Saltiamo la cartella radice
        if relative_path == "":
            continue

        path = PurePosixPath(relative_path)

        resource_type = response.find(
            "d:propstat/d:prop/d:resourcetype",
            NS,
        )

        prop = response.find(
            "d:propstat/d:prop",
            NS,
        )
        
        size = None
        modified = None
        etag = None
        
        if prop is not None:
        
            size_node = prop.find(
                "d:getcontentlength",
                NS,
            )
        
            if (
                size_node is not None
                and size_node.text
            ):
                size = int(size_node.text)
        
            modified_node = prop.find(
                "d:getlastmodified",
                NS,
            )
        
            if (
                modified_node is not None
                and modified_node.text
            ):
                modified = modified_node.text
        
            etag_node = prop.find(
                "d:getetag",
                NS,
            )
        
            if (
                etag_node is not None
                and etag_node.text
            ):
                etag = etag_node.text.strip('"')

        

        is_dir = False

        if resource_type is not None:
            is_dir = (
                resource_type.find(
                    "d:collection",
                    NS,
                )
                is not None
            )

        item = WebDAVItem(
            name=path.name,
            path=relative_path,
            is_dir=is_dir,
            size=size,
            last_modified=modified,
            etag=etag,
        )

        items.append(item)

    return items