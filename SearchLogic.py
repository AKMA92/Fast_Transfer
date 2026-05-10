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

    def find_sprinter_by_names(
            self,
            start_name,
            transfer_name,
            target_name
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

        # 2. Sprinter mit IDs suchen
        self.find_sprinter_via_transfer(
            start_id,
            transfer_id,
            target_id,
            start_name,
            transfer_name,
            target_name
        )

    def find_sprinter_via_transfer(
            self,
            start_id,
            transfer_id,
            target_id,
            start_name,
            transfer_name,
            target_name
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

        # 4. Wartezeit berechnen
        print(f"\nSprinter-Verbindungen {start_name} -> {transfer_name} -> {target_name}:\n")

        found = False

        for first_trip in start_to_transfer:
            arrival_transfer = self.time_to_minutes(
                first_trip["arrival_transfer"]
            )

            for second_trip in transfer_to_target:
                departure_transfer = self.time_to_minutes(
                    second_trip["departure_transfer"]
                )

                waiting_time = departure_transfer - arrival_transfer

                if 2 <= waiting_time <= 3:
                    found = True

                    print("Sprinter gefunden:")
                    print(f"Trip 1: {first_trip['trip_id']}")
                    print(f"Ab {start_name}: {first_trip['departure_start']}")
                    print(f"An {transfer_name}: {first_trip['arrival_transfer']}")
                    print(f"Umsteigezeit: {waiting_time} Minuten")
                    print(f"Trip 2: {second_trip['trip_id']}")
                    print(f"Ab {transfer_name}: {second_trip['departure_transfer']}")
                    print(f"An {target_name}: {second_trip['arrival_target']}")
                    print("-" * 50)

        if not found:
            print("Keine Sprinter-Verbindung mit 2–3 Minuten Umsteigezeit gefunden.")


if __name__ == "__main__":
    search = SearchLogic()

    search.find_sprinter_by_names(
        "Winterthur",
        "Zürich HB",
        "Horgen"
    )