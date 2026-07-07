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