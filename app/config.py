import os
from dataclasses import dataclass
from pathlib import Path

import yaml

@dataclass
class NextcloudConfig:
    url: str
    username: str
    password: str


@dataclass
class PhoneConfig:
    name: str
    source: str


@dataclass
class AppConfig:
    nextcloud: NextcloudConfig
    phones: list[PhoneConfig]
    dry_run: bool = True


def load_config() -> AppConfig:
    config_file = Path(
        os.getenv(
            "CONFIG_FILE",
            "config.yml",
        )
    )

    with config_file.open(
        "r",
        encoding="utf-8",
    ) as file:
        data = yaml.safe_load(file)

    nextcloud = NextcloudConfig(
        url=data["nextcloud"]["url"],
        username=data["nextcloud"]["username"],
        password=data["nextcloud"]["password"],
    )

    phones = [
        PhoneConfig(**phone)
        for phone in data["phones"]
    ]

    return AppConfig(
        nextcloud=nextcloud,
        phones=phones,
        dry_run=data.get("dry_run", True),
    )