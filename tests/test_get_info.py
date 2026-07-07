from app.config import load_config
from app.webdav import WebDAVClient


config = load_config()

client = WebDAVClient(
    url=config.nextcloud.url,
    username=config.nextcloud.username,
    password=config.nextcloud.password,
)

item = client.get_info(
    "Foto/Backup Phone Gian/test2.jpg"
)

print(item)

client.move(
    "Foto/Backup Phone Gian/test2.jpg",
    "Foto/Backup Phone Gian/Test/test2.jpg",
)