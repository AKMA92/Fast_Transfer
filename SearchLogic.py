import pandas as pd


class SearchLogic:

    def __init__(self):
        self.stops = pd.read_csv(
            "gtfs_data/stops.txt",
            sep=";",
            low_memory=False
        )

        self.stop_times = pd.read_csv(
            "gtfs_data/stop_times.txt",
            sep=","
        )

        self.stops.columns = self.stops.columns.str.strip()
        self.stop_times.columns = self.stop_times.columns.str.strip()

    def find_stop_id(self, stop_name):
        result = self.stops[
            self.stops["stop_name"].str.lower() == stop_name.lower()
        ]

        if result.empty:
            print(f"Keine Station gefunden: {stop_name}")
            return None

        stop_id = result.iloc[0]["stop_id"]
        return stop_id

    def time_to_minutes(self, time_text):
        parts = time_text.split(":")
        hours = int(parts[0])
        minutes = int(parts[1])

        return hours * 60 + minutes

    def find_connection_by_names(
            self,
            start_name,
            transfer_name,
            target_name,
            is_sprinter=False
    ):
        # 1. Namen in stop_id umwandeln
        start_id = self.find_stop_id(start_name)
        transfer_id = self.find_stop_id(transfer_name)
        target_id = self.find_stop_id(target_name)

        if start_id is None or transfer_id is None or target_id is None:
            print("Mindestens eine Station wurde nicht gefunden.")
            return

        print("Gefundene IDs:")
        print(f"{start_name}: {start_id}")
        print(f"{transfer_name}: {transfer_id}")
        print(f"{target_name}: {target_id}")

        # 2. Verbindung suchen
        self.find_connection_via_transfer(
            start_id,
            transfer_id,
            target_id,
            start_name,
            transfer_name,
            target_name,
            is_sprinter
        )

    def find_connection_via_transfer(
            self,
            start_id,
            transfer_id,
            target_id,
            start_name,
            transfer_name,
            target_name,
            is_sprinter=False
    ):
        relevant_stops = self.stop_times[
            self.stop_times["stop_id"].isin(
                [start_id, transfer_id, target_id]
            )
        ]

        grouped = relevant_stops.groupby("trip_id")

        start_to_transfer = []
        transfer_to_target = []

        # 3. Trips suchen: Start -> Umstieg und Umstieg -> Ziel
        for trip_id, group in grouped:
            stop_ids = group["stop_id"].tolist()

            if start_id in stop_ids and transfer_id in stop_ids:
                start_row = group[group["stop_id"] == start_id].iloc[0]
                transfer_row = group[group["stop_id"] == transfer_id].iloc[0]

                if start_row["stop_sequence"] < transfer_row["stop_sequence"]:
                    start_to_transfer.append({
                        "trip_id": trip_id,
                        "departure_start": start_row["departure_time"],
                        "arrival_transfer": transfer_row["arrival_time"]
                    })

            if transfer_id in stop_ids and target_id in stop_ids:
                transfer_row = group[group["stop_id"] == transfer_id].iloc[0]
                target_row = group[group["stop_id"] == target_id].iloc[0]

                if transfer_row["stop_sequence"] < target_row["stop_sequence"]:
                    transfer_to_target.append({
                        "trip_id": trip_id,
                        "departure_transfer": transfer_row["departure_time"],
                        "arrival_target": target_row["arrival_time"]
                    })

        # 4. Je nach Modus andere Umsteigezeit verwenden
        if is_sprinter:
            min_waiting_time = 2
            max_waiting_time = 5
            search_type = "Sprinter-Verbindungen"
        else:
            min_waiting_time = 2
            max_waiting_time = 30
            search_type = "Normale Verbindungen"

        print(f"\n{search_type} {start_name} -> {transfer_name} -> {target_name}:\n")

        found = False

        # 5. Beide Trip-Listen vergleichen
        for first_trip in start_to_transfer:
            arrival_transfer = self.time_to_minutes(
                first_trip["arrival_transfer"]
            )

            for second_trip in transfer_to_target:
                departure_transfer = self.time_to_minutes(
                    second_trip["departure_transfer"]
                )

                waiting_time = departure_transfer - arrival_transfer

                # 6. Prüfen, ob die Wartezeit zum Modus passt
                if min_waiting_time <= waiting_time <= max_waiting_time:
                    found = True

                    print("Verbindung gefunden:")
                    print(f"Trip 1: {first_trip['trip_id']}")
                    print(f"Ab {start_name}: {first_trip['departure_start']}")
                    print(f"An {transfer_name}: {first_trip['arrival_transfer']}")
                    print(f"Umsteigezeit: {waiting_time} Minuten")
                    print(f"Trip 2: {second_trip['trip_id']}")
                    print(f"Ab {transfer_name}: {second_trip['departure_transfer']}")
                    print(f"An {target_name}: {second_trip['arrival_target']}")
                    print("-" * 50)

        if not found:
            print(f"Keine passende Verbindung gefunden.")

"""
if __name__ == "__main__":
    search = SearchLogic()

    # Normale Suche: 2 bis 30 Minuten Umsteigezeit
    search.find_connection_by_names(
        "Winterthur",
        "Zürich HB",
        "Horgen",
        is_sprinter=False
    )

    # Sprinter-Suche: 2 bis 5 Minuten Umsteigezeit
    search.find_connection_by_names(
        "Winterthur",
        "Zürich HB",
        "Horgen",
        is_sprinter=True
    )

"""