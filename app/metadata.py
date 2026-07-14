import re

from app.models import (
    WebDAVItem,
    PhotoDate,
)
from email.utils import parsedate_to_datetime

DATE_PATTERN = re.compile(
    r"(20\d{2})(0[1-9]|1[0-2])(?:0[1-9]|[12]\d|3[01])"
)


class MetadataExtractor:


    def get_date(self, item) -> PhotoDate | None:
    
        date = self.get_date_from_filename(item)
    
        if date is not None:
            return date
    
        if item.last_modified:
    
            try:
    
                dt = parsedate_to_datetime(
                    item.last_modified
                )
    
                return PhotoDate(
                    year=dt.year,
                    month=dt.month,
                )
    
            except Exception:
                pass
    
        return None

    def get_date_from_filename(
        self,
        item: WebDAVItem,
    ) -> PhotoDate | None:
    
        match = DATE_PATTERN.search(item.name)
    
        if match is None:
            return None
    
        return PhotoDate(
            year=int(match.group(1)),
            month=int(match.group(2)),
        )