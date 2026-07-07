import httpx
from pathlib import PurePosixPath
from urllib.parse import quote

from app.parser import parse_propfind


class WebDAVClient:

    def __init__(self, url: str, username: str, password: str):
        self.url = url.rstrip("/")
        self.username = username
        self.password = password

        self.webdav_root = (
            f"/remote.php/dav/files/{self.username}/"
        )

        self.session = httpx.Client(
            auth=(self.username, self.password),
            timeout=30,
            follow_redirects=True,
        )

    def server_info(self):
        return self._request("GET")

    def list_directory(self, path: str = ""):

        response = self._request(
            method="PROPFIND",
            path=path,
            headers={
                "Depth": "1",
            },
        )

        response.raise_for_status()

        return parse_propfind(
            response.text,
            self.webdav_root,
            path,
        )

    def get_info(self, path: str):

        response = self._request(
            method="PROPFIND",
            path=path,
            headers={
                "Depth": "0",
            },
        )

        if response.status_code == 404:
            return None

        response.raise_for_status()

        parent = str(PurePosixPath(path).parent)

        items = parse_propfind(
            response.text,
            self.webdav_root,
            parent,
        )

        if not items:
            return None

        return items[0]

    def mkdir(self, path: str):

        response = self._request(
            method="MKCOL",
            path=path,
        )

        if response.status_code in (201, 405):
            return

        response.raise_for_status()

    def move(
        self,
        source: str,
        destination: str,
    ):

        destination_url = (
            f"{self.url}"
            f"{self.webdav_root}"
            f"{quote(destination.strip('/'), safe='/')}"
        )

        response = self._request(
            method="MOVE",
            path=source,
            headers={
                "Destination": destination_url,
                "Overwrite": "F",
            },
        )

        response.raise_for_status()

    def delete(
        self,
        path: str,
    ):
    
        response = self._request(
            method="DELETE",
            path=path,
        )
    
        response.raise_for_status()

    def download(self, path: str):
        pass

    def _request(
        self,
        method: str,
        path: str = "",
        headers: dict | None = None,
    ):

        headers = headers or {}

        path = path.strip("/")

        url = f"{self.url}{self.webdav_root}"

        if path:
            url += quote(path, safe="/")

        response = self.session.request(
            method=method,
            url=url,
            headers=headers,
        )

        return response