from Downloader import Downloader


class Application:

    def __init__(self):
        pass

    def main(self):
        downloader = Downloader()
        downloader.get_data()


if __name__ == "__main__":
    app = Application()
    app.main()