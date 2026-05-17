import pandas as pd


class SearchLogic:

    def __init__(self):
        pass

    def load_csv(self):
        self.stops = pd.read_csv(
            "gtfs_data/stops.txt",
            sep=",",
            low_memory=False
        )

        self.stop_times = pd.read_csv(
            "gtfs_data/stop_times.txt",
            sep=","
        )

        self.stops.columns = self.stops.columns.str.strip()
        self.stop_times.columns = self.stop_times.columns.str.strip()


    def find_stop_ids(self, stop_name):
        result = self.stops[
            self.stops["stop_name"].str.strip().str.lower()
            == stop_name.strip().lower()
        ]

        if result.empty:
            return None

        stop_ids = result["stop_id"].tolist()
        return stop_ids

    def time_to_minutes(self, time_text):
        if not isinstance(time_text, str):
            return None

        parts = time_text.split(":")

        if len(parts) < 2:
            return None

        hours = int(parts[0])
        minutes = int(parts[1])

        return hours * 60 + minutes

    def find_connection_by_names(
            self,
            start_name,
            transfer_name,
            target_name,
            date,
            time,
            is_sprinter=False
    ):
        self.load_csv()

        start_ids = self.find_stop_ids(start_name)
        transfer_ids = self.find_stop_ids(transfer_name)
        target_ids = self.find_stop_ids(target_name)

        if start_ids is None or transfer_ids is None or target_ids is None:
            return ["Mindestens eine Station wurde nicht gefunden."]

        return self.find_connection_via_transfer(
            start_ids,
            transfer_ids,
            target_ids,
            start_name,
            transfer_name,
            target_name,
            date,
            time,
            is_sprinter
        )

    def find_connection_via_transfer(
            self,
            start_ids,
            transfer_ids,
            target_ids,
            start_name,
            transfer_name,
            target_name,
            date,
            time,
            is_sprinter=False
    ):
        selected_time = self.time_to_minutes(time)

        if selected_time is None:
            return ["Ungültige Zeit. Erwartetes Format: HH:MM:SS"]

        all_stop_ids = start_ids + transfer_ids + target_ids

        relevant_stops = self.stop_times[
            self.stop_times["stop_id"].isin(all_stop_ids)
        ]

        grouped = relevant_stops.groupby("trip_id")

        start_to_transfer = []
        transfer_to_target = []

        for trip_id, group in grouped:
            stop_ids = group["stop_id"].tolist()

            has_start = any(stop_id in stop_ids for stop_id in start_ids)
            has_transfer = any(stop_id in stop_ids for stop_id in transfer_ids)

            if has_start and has_transfer:
                start_row = group[group["stop_id"].isin(start_ids)].iloc[0]
                transfer_row = group[group["stop_id"].isin(transfer_ids)].iloc[0]

                if start_row["stop_sequence"] < transfer_row["stop_sequence"]:
                    departure_start_minutes = self.time_to_minutes(
                        start_row["departure_time"]
                    )

                    if departure_start_minutes is None:
                        continue

                    if departure_start_minutes >= selected_time:
                        start_to_transfer.append({
                            "trip_id": trip_id,
                            "departure_start": start_row["departure_time"],
                            "arrival_transfer": transfer_row["arrival_time"],
                            "date": date
                        })

            has_transfer = any(stop_id in stop_ids for stop_id in transfer_ids)
            has_target = any(stop_id in stop_ids for stop_id in target_ids)

            if has_transfer and has_target:
                transfer_row = group[group["stop_id"].isin(transfer_ids)].iloc[0]
                target_row = group[group["stop_id"].isin(target_ids)].iloc[0]

                if transfer_row["stop_sequence"] < target_row["stop_sequence"]:
                    transfer_to_target.append({
                        "trip_id": trip_id,
                        "departure_transfer": transfer_row["departure_time"],
                        "arrival_target": target_row["arrival_time"],
                        "date": date
                    })

        if is_sprinter:
            min_waiting_time = 1
            max_waiting_time = 30
            search_type = "Kritische Sprinter-Verbindungen"
        else:
            min_waiting_time = 5
            max_waiting_time = 30
            search_type = "Normale Verbindungen"

        result_list = []

        result_list.append(
            f"{search_type} am {date}: "
            f"{start_name} -> {transfer_name} -> {target_name}"
        )

        connections = []
        seen_connections = set()

        for first_trip in start_to_transfer:
            arrival_transfer = self.time_to_minutes(first_trip["arrival_transfer"])
            departure_start = self.time_to_minutes(first_trip["departure_start"])

            if arrival_transfer is None or departure_start is None:
                continue

            for second_trip in transfer_to_target:
                departure_transfer = self.time_to_minutes(
                    second_trip["departure_transfer"]
                )

                if departure_transfer is None:
                    continue

                waiting_time = departure_transfer - arrival_transfer

                if waiting_time <= 4:
                    status = "CRITICAL"
                elif waiting_time <= 6:
                    status = "TIGHT"
                else:
                    status = "SAFE"

                if min_waiting_time <= waiting_time <= max_waiting_time:

                    # Duplikate vermeiden:
                    # Wenn Startzeit, Ankunft Umstieg, Abfahrt Umstieg und Zielzeit gleich sind,
                    # wird die Verbindung nur einmal angezeigt.
                    connection_key = (
                        first_trip["departure_start"],
                        first_trip["arrival_transfer"],
                        second_trip["departure_transfer"],
                        second_trip["arrival_target"]
                    )

                    if connection_key in seen_connections:
                        continue

                    seen_connections.add(connection_key)

                    connections.append({
                        "departure_start_minutes": departure_start,
                        "first_trip": first_trip,
                        "second_trip": second_trip,
                        "waiting_time": waiting_time,
                        "status": status
                    })

        connections.sort(key=lambda x: x["departure_start_minutes"])

        for connection in connections[:10]:
            first_trip = connection["first_trip"]
            second_trip = connection["second_trip"]

            result_text = (
                "Verbindung gefunden:\n"
                f"Datum: {date}\n"
                f"Trip 1: {first_trip['trip_id']}\n"
                f"Ab {start_name}: {first_trip['departure_start']}\n"
                f"An {transfer_name}: {first_trip['arrival_transfer']}\n"
                f"Umsteigezeit: {connection['waiting_time']} Minuten\n"
                f"Status: {connection['status']}\n"
                f"Trip 2: {second_trip['trip_id']}\n"
                f"Ab {transfer_name}: {second_trip['departure_transfer']}\n"
                f"An {target_name}: {second_trip['arrival_target']}\n"
                + "-" * 50
            )

            result_list.append(result_text)

        if len(result_list) == 1:
            result_list.append("Keine passende Verbindung gefunden.")

        return result_list