"""
SearchLogic – Ablauf der Sprinter-Suche

Ziel:
Das Programm sucht sogenannte "Sprinter-Verbindungen".
Das sind Verbindungen mit einem sehr kurzen Umstieg
(z. B. 2–3 Minuten).

Beispiel:
Winterthur -> Zürich HB -> Horgen

Das Programm arbeitet mit GTFS-Daten.
GTFS beschreibt Fahrpläne von Zügen und Bussen.

Wichtige Dateien:

1. stops.txt
Enthält alle Stationen.
Wichtige Spalten:
- stop_id
- stop_name

Beispiel:
8506000 = Winterthur
8503000 = Zürich HB

----------------------------------------------------

2. stop_times.txt
Enthält alle Halte eines Trips.
Wichtige Spalten:
- trip_id
- arrival_time
- departure_time
- stop_id
- stop_sequence

Ein trip_id beschreibt eine komplette Zugfahrt.

Beispiel:
Trip 100 fährt:
Winterthur -> Zürich -> Aarau

----------------------------------------------------

Programmablauf:

1. Der Benutzer gibt 3 Stationen ein:
- Startstation
- Umstiegsstation
- Zielstation

Beispiel:
Winterthur
Zürich HB
Horgen

----------------------------------------------------

2. Das Programm sucht die passenden stop_ids
in stops.txt.

Beispiel:
Winterthur -> 8506000
Zürich HB -> 8503000
Horgen -> 8503855

----------------------------------------------------

3. Das Programm filtert stop_times.txt
und sucht nur relevante Daten
für diese 3 Stationen.

----------------------------------------------------

4. Danach werden alle Zeilen nach trip_id gruppiert.

Dadurch sieht das Programm:
Welche Stationen gehören zur gleichen Zugfahrt?

----------------------------------------------------

5. Jetzt sucht das Programm zwei verschiedene Trips:

Trip A:
Startstation -> Umstiegsstation

Beispiel:
Winterthur -> Zürich HB

Trip B:
Umstiegsstation -> Zielstation

Beispiel:
Zürich HB -> Horgen

----------------------------------------------------

6. Für beide Trips werden Zeiten gespeichert:

Trip A:
Ankunft bei Umstiegsstation

Trip B:
Abfahrt bei Umstiegsstation

----------------------------------------------------

7. Danach berechnet das Programm
die Umsteigezeit.

Beispiel:
Ankunft Zürich HB = 08:21
Abfahrt Zürich HB = 08:23

Wartezeit:
08:23 - 08:21 = 2 Minuten

----------------------------------------------------

8. Wenn die Umsteigezeit zwischen
2 und 3 Minuten liegt,
wird die Verbindung als
"Sprinter-Verbindung" ausgegeben.

----------------------------------------------------

Wichtige Erkenntnis:

Ein einzelner trip_id reicht nicht aus,
weil bei einer Umsteigeverbindung
mindestens zwei verschiedene Trips existieren.

Darum:
Trip A + Trip B müssen kombiniert werden.
"""