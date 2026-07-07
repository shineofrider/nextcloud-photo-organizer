from dataclasses import dataclass


@dataclass
class NextcloudConfig:
    url: str
    username: str
    password: str


@dataclass
class AppConfig:
    nextcloud: NextcloudConfig
    phones: list[str]

from pathlib import Path
import yaml

# ... dataclass ...


def load_config() -> AppConfig:
    config_file = Path("config.yml")

    with config_file.open(
        "r",
        encoding="utf-8"
    ) as file:

        data = yaml.safe_load(file)
        nextcloud = NextcloudConfig(
            url=data["nextcloud"]["url"],
            username=data["nextcloud"]["username"],
            password=data["nextcloud"]["password"]
            
        )
        config = AppConfig(
            nextcloud=nextcloud,
            phones=data["phones"],
      )

    return config