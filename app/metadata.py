import re

from app.models import WebDAVItem
from email.utils import parsedate_to_datetime

YEAR_PATTERN = re.compile(r"(19|20)\d{2}")


class MetadataExtractor:


    def get_year(self, item):
    
        year = self.get_year_from_filename(item)
    
        if year is not None:
            return year
    
        if item.last_modified:
        
            try:
                return parsedate_to_datetime(
                    item.last_modified
                ).year
    
            except Exception:
                pass
            
        return None

    def get_year_from_filename(
        self,
        item: WebDAVItem,
    ) -> int | None:

        match = YEAR_PATTERN.search(item.name)

        if match is None:
            return None

        return int(match.group())