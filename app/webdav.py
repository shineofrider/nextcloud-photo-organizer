import httpx
from urllib.parse import quote
from parser import parse_propfind

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
        )

        return parse_propfind(
            response.text,
            self.webdav_root,
        )

    def move(self, source, destination):
        pass

    def mkdir(self, path):
        pass

    def download(self, path):
        pass
    
    def _request(self, method: str, path: str = ""):
        path = path.strip("/")

        url = f"{self.url}{self.webdav_root}"

        if path:
            url += quote(path)

        headers = {}

        if method == "PROPFIND":
            headers["Depth"] = "1"

        response = self.session.request(
            method=method,
            url=url,
            headers=headers,
        )

        return response