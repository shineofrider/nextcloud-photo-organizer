from webdav import WebDAVClient

from config import load_config

def main():
    config = load_config()

    client = WebDAVClient(
        url=config.nextcloud.url,
        username=config.nextcloud.username,
        password=config.nextcloud.password,
    )

    items = client.list_directory()

    print(items)

if __name__ == "__main__":
    main()
    