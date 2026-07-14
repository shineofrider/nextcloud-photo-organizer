from app.config import AppConfig
from app.webdav import WebDAVClient
from pathlib import PurePosixPath
from app.metadata import MetadataExtractor
from app.models import MoveOperation


SUPPORTED_EXTENSIONS = {
    ".jpg",
    ".jpeg",
    ".heic",
    ".png",
    ".mp4",
    ".mov",
    ".dng",
    ".avi",
    ".gif",
}

class PhotoOrganizer:
    def is_supported_photo(self, item):

        if item.is_dir:
            return False

        extension = PurePosixPath(item.name).suffix.lower()

        return extension in SUPPORTED_EXTENSIONS

    def __init__(self, config: AppConfig):

        self.config = config

        self.client = WebDAVClient(
            url=config.nextcloud.url,
            username=config.nextcloud.username,
            password=config.nextcloud.password,
        )

        self.metadata = MetadataExtractor()
        
        self.created_folders: set[str] = set()

    def run(self):

        print("Photo Organizer avviato")

        for phone in self.config.phones:

            self.process_phone(phone)

            
    def process_phone(self, phone):
    
        print()
    
        print("=" * 40)
        print(f"Telefono: {phone.name}")
        print("=" * 40)
    
        items = self.client.list_directory(phone.source)
    
        photos = [
            item
            for item in items
            if self.is_supported_photo(item)
        ]
    
        groups = self.group_by_period(photos)
    
        operations = self.build_move_plan(
            phone,
            groups,
        )
    
        move_count = 0
        duplicate_count = 0
        conflict_count = 0
        error_count = 0
    
        print()
        print("ELABORAZIONE")
        print("-" * 40)
    
        for operation in operations:
    
            try:

                destination = self.client.get_info(
                    operation.destination_path
                )
    
                # ==========================
                # Caso 1: il file non esiste
                # ==========================
                if destination is None:
    
                    folder = str(
                        PurePosixPath(
                            operation.destination_path
                        ).parent
                    )
    
                    if not self.config.dry_run:
                    
                        if folder not in self.created_folders:

                            self.client.mkdir(folder)
                    
                            self.created_folders.add(folder)
                    
                        self.client.move(
                            f"{phone.source}/{operation.source.path}",
                            operation.destination_path,
                        )
    
                    print("[MOVE]")
                    print(f"{phone.source}/{operation.source.path}")
                    print("↓")
                    print(operation.destination_path)
                    print()
    
                    move_count += 1
    
                # ==========================
                # Caso 2: file identico
                # ==========================
                elif (
                    destination.size == operation.source.size
                    and destination.etag == operation.source.etag
                ):
    
                    if not self.config.dry_run:
    
                        self.client.delete(
                            f"{phone.source}/{operation.source.path}"
                        )
    
                    print(f"[DUPLICATE] {operation.source.name}")
    
                    duplicate_count += 1
    
                # ==========================
                # Caso 3: conflitto
                # ==========================
                else:
    
                    print("[CONFLICT]")
                    print(f"Sorgente     : {phone.source}/{operation.source.path}")
                    print(f"Destinazione : {operation.destination_path}")
                    print(f"Size         : {operation.source.size} -> {destination.size}")
                    print(f"ETag         : {operation.source.etag} -> {destination.etag}")
                    print()
    
                    conflict_count += 1
    
            except Exception as ex:
    
                print(f"[ERROR] {operation.source.name}")
                print(ex)
                print()
    
                error_count += 1
    
        print()
        print("=" * 40)
    
        print(f"Foto trovate : {len(photos)}")
        print(f"Spostate     : {move_count}")
        print(f"Duplicati    : {duplicate_count}")
        print(f"Conflitti    : {conflict_count}")
        print(f"Errori       : {error_count}")


    def group_by_period(self, photos):
    
        groups = {}
    
        for photo in photos:
    
            date = self.metadata.get_date(photo)
    
            if date is None:
                continue
    
            key = (
                date.year,
                date.month,
            )
    
            if key not in groups:
                groups[key] = []
    
            groups[key].append(photo)
    
        return groups
    
    def build_move_plan(self, phone, groups):
    
        operations = []
    
        for (year, month), photos in groups.items():
    
            for photo in photos:
    
                source = f"{phone.source}/{photo.path}"
                
                destination = (
                    f"{phone.source}/"
                #    f"{PurePosixPath(phone.source).parent}/"
                    f"{year}/"
                    f"{month:02d}/"
                    f"{photo.name}"
                )
                
                if source == destination:
                    continue
                
                operations.append(
                    MoveOperation(
                        source=photo,
                        destination_path=destination,
                    )
                )
    
        return operations