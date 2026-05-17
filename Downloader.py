import requests
import time
import os
import zipfile


class Downloader:

    url = "https://data.opentransportdata.swiss/dataset/3d2c18f9-9ef1-463f-a249-5c67604efd74/resource/42e4a546-ab9d-41b7-b7ce-cc0ef4c0e0f3/download/gtfs_fp2026_20260503.zip"
    zip_file = "gtfs.zip"
    target_folder = "gtfs_data"

    def __init__(self):
        pass

    def get_data(self):
        # Prüfen, ob ZIP-Datei existiert
        if os.path.exists(self.zip_file):
        #if False:
            file_time = os.stat(self.zip_file).st_mtime
            current_time = time.time()
            age = current_time - file_time
            print("age:", age)

            # Wenn ZIP-Datei jünger als 10 Minuten ist -> Cache benutzen
            if age < 600:
            #if 1 < 2:
                print("Benutze Cache-ZIP")
                #self.unzip_file()
                return self.target_folder

        # Sonst neue ZIP-Datei laden
        retries = 4
        print("Retries:", retries)

        for attempt in range(retries):
            try:
                response = requests.get(self.url)
                response.raise_for_status()

                # ZIP-Datei speichern
                with open(self.zip_file, "wb") as file:
                    file.write(response.content)

                print("ZIP-Datei wurde heruntergeladen")

                # ZIP-Datei entpacken
                self.unzip_file()

                return self.target_folder

            except Exception as e:
                print(f"Fehler bei Versuch {attempt + 1}: {e}")

                wait_time = 2 ** attempt
                print(f"Warte {wait_time} Sekunden...")
                time.sleep(wait_time)

        print("Maximale Versuche erreicht")
        return None

    def unzip_file(self):
        os.makedirs(self.target_folder, exist_ok=True)

        with zipfile.ZipFile(self.zip_file, "r") as zip_ref:
            zip_ref.extractall(self.target_folder)

        print("ZIP-Datei wurde entpackt")
