from app.config import load_config
from app.organizer import PhotoOrganizer


def main():

    config = load_config()

    organizer = PhotoOrganizer(config)

    organizer.run()


if __name__ == "__main__":
    main()