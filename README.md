# Fast_Transfer

Dieses Projekt implementiert eine einfache Sprinter-Suche mit GTFS-Daten der SBB.

Das Programm sucht Verbindungen mit einem Umstieg und sehr kurzer Umsteigezeit (2–3 Minuten).

Dafür werden Stationen aus `stops.txt` und Fahrzeiten aus `stop_times.txt` analysiert.

Die Logik kombiniert zwei verschiedene Trips:

- Start -> Umstieg
- Umstieg -> Ziel

## GTFS Datenmodell

![GTFS Datenmodell](images/gtfs_model.png)