import re

from app.models import WebDAVItem

YEAR_PATTERN = re.compile(r"(19|20)\d{2}")


class MetadataExtractor:

    def get_year(self, item: WebDAVItem) -> int | None:

        year = self.get_year_from_filename(item)

        if year is not None:
            return year

        return None

    def get_year_from_filename(
        self,
        item: WebDAVItem,
    ) -> int | None:

        match = YEAR_PATTERN.search(item.name)

        if match is None:
            return None

        return int(match.group())