import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout,
    QHBoxLayout, QLabel, QPushButton, QComboBox,
    QLineEdit, QCheckBox, QWidget, QTextEdit, QDateTimeEdit
)
from PySide6.QtCore import QDateTime, QDate

from Downloader import Downloader
from SearchLogic import SearchLogic

class Application (QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Fast Transfer - Fahrplanapp")
        self.setMinimumSize(888, 666)
        self.build_ui()

    def build_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(10)
        main_layout.setContentsMargins(30, 30, 30, 30)
# Titel
        title = QLabel("Fast Transfer - Fahrplanapp")
        title.setStyleSheet("font-size: 20px; font-weight: bold;")
        main_layout.addWidget(title)
# Datum-DropDown
        filter_layout = QHBoxLayout()

        self.input_datum = QDateTimeEdit ()
        self.input_datum.setDate(QDate.currentDate())
        self.input_datum.setDisplayFormat("dd.MM.yyyy")
        self.input_datum.setCalendarPopup(True)
        filter_layout.addWidget(QLabel("Datum:"))
        filter_layout.addWidget(self.input_datum)
# Abfahrtszeit-DropDown
        self.input_time = QComboBox()
        current_hour = QDateTime.currentDateTime().time().hour()
        current_minute = QDateTime.currentDateTime().time().minute()

        for hour in range(0, 24):
            for minute in [0, 15, 30, 45, ]:
                self.input_time.addItem(f"{hour:02d}:{minute:02d} Uhr")

        closest = f"{current_hour:02d}:{(current_minute // 15) * 15:02d} Uhr"
        index = self.input_time.findText(closest)
        self.input_time.setCurrentIndex(index)
        filter_layout.addWidget(QLabel("Abfahrtszeit:"))
        filter_layout.addWidget(self.input_time)
 # Sprinter-Checkbox
        self.checkbox_sprinter = QCheckBox("Sprinter-Modus (aktiviert kurze Umstiegszeiten)")
        filter_layout.addWidget(self.checkbox_sprinter)

        filter_layout.addStretch()
        main_layout.addLayout(filter_layout)

# Eingabefelder
        self.input_start = QLineEdit()
        self.input_start.setPlaceholderText("Startstation z.B. Winterthur")
        self.input_transfer = QLineEdit()
        self.input_transfer.setPlaceholderText("Transfer z.B. Zürich HB")
        self.input_end = QLineEdit()
        self.input_end.setPlaceholderText("Endstation z.B. Thalwil")

        main_layout.addWidget(QLabel("Start:"))
        main_layout.addWidget(self.input_start)
        main_layout.addWidget(QLabel("Umstieg:"))
        main_layout.addWidget(self.input_transfer)
        main_layout.addWidget(QLabel("Ziel:"))
        main_layout.addWidget(self.input_end)
# Such-Button
        self.btn_search = QPushButton("Verbindung suchen")
        self.btn_search.setStyleSheet("font-size: 14px; padding: 8px; background-color: red;")
        main_layout.addWidget(self.btn_search)
# Ergebnisse
        self.results = QTextEdit()
        self.results.setReadOnly(True)
        self.results.setStyleSheet("background-color: white; color: black;")
        self.results.setPlaceholderText("Hier erscheinen die Verbindungen...")
        main_layout.addWidget(QLabel("Verbindungen:"))
        main_layout.addWidget(self.results)
#Connection
        self.btn_search.clicked.connect(self.on_search)

        self.input_start.returnPressed.connect(self.input_transfer.setFocus)
        self.input_transfer.returnPressed.connect(self.input_end.setFocus)
        self.input_end.returnPressed.connect(self.btn_search.click)

    def on_search(self):
        start = self.input_start.text()
        transfer = self.input_transfer.text()
        end = self.input_end.text()
        is_sprinter = self.checkbox_sprinter.isChecked()

        if not start or not transfer or not end:
            self.results.setText("Bitte alle Felder ausfüllen.")
            return
        try:
            self.search.find_connection_by_names(start, transfer, end, is_sprinter)
        except Exception as e:
            self.results.setText(f"Fehler: {str(e)}")

        #self.results.setText(f"Suche: {start} => {transfer} => {end} (Sprinter-Modus: {is_sprinter})")

    def main(self):
        downloader = Downloader()
        self.search = SearchLogic()
        downloader.get_data()

        # @Marvin hier kannst du dein GUI Objekt erzeugen
        # gui = Gui()
        # Funktionen aufrufen
        # Lädt alle gtfs Daten herunter ins Projekt, (enzipt, erstellt Ordner)
        # @Marvin ein Beispiel wie du die SuchLogic ansteuern kannst (Params beachten)
        # Das Result ist aktuell noch in der Console.
        # Ich später wirst du ein String Array oder so als Return erhalten was du dann als Ausgabe verarbeiten kannst in deinem GUI
        #self.search.find_connection_by_names("Winterthur","Zürich HB","Horgen",is_sprinter=False)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Application()
    window.show()
    window.main()
    sys.exit(app.exec())