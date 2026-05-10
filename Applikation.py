from Downloader import Downloader
from SearchLogic import SearchLogic

class Application:

    # Einstiegspunkt System
    def main(self):
        # Alle Objecte erzeugen
        downloader = Downloader()
        search = SearchLogic()
        # @Marvin hier kannst du dein GUI Objekt erzeugen
        # gui = Gui()

        # Funktionen aufrufen
        # Lädt alle gtfs Daten herunter ins Projekt, (enzipt, erstellt Ordner)
        downloader.get_data()

        # @Marvin ein Beispiel wie du die SuchLogic ansteuern kannst (Params beachten)
        # Das Result ist aktuell noch in der Console.
        # Ich später wirst du ein String Array oder so als Return erhalten was du dann als Ausgabe verarbeiten kannst in deinem GUI
        search.find_connection_by_names("Winterthur","Zürich HB","Horgen",is_sprinter=False)

if __name__ == "__main__":
    app = Application()
    app.main()