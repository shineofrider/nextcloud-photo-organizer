from app.models import (
    WebDAVItem,
    SyncDecision,
)


class FileComparer:

    def compare(
        self,
        source: WebDAVItem,
        destination: WebDAVItem | None,
    ) -> SyncDecision:

        if destination is None:
            return SyncDecision.MOVE

        if source.size != destination.size:
            return SyncDecision.CONFLICT

        if source.etag == destination.etag:
            return SyncDecision.DELETE_DUPLICATE

        return SyncDecision.CONFLICT