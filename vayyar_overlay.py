from yaml import safe_load

from db_driver import DbDriver


class VayyarOverlay:
    def __init__(self, min_ts: int, max_ts: int):
        self.min = min_ts
        self.max = max_ts
        self.db_room = DbDriver(keys=self._get_keys(), table='vayyar_home_c2c_room_status')
        self._data = self._get_room_data(youngest_ts=min_ts, oldest_ts=max_ts)

    def get_overlay_data(self) -> dict:
        data = {"data": self._data, "min": self._data[0].get("timestamp"), "max": self._data[-1].get("timestamp"),
                "label": "vayyar", "color": "orange"}
        return data

    @staticmethod
    def _get_keys():
        with open("keys.yml") as config_file:
            return safe_load(config_file)

    def _get_room_data(self, oldest_ts, youngest_ts) -> list:
        cloud_data = self.db_room.query_db(oldest_timestamp=oldest_ts, untill_timestamp=youngest_ts)
        return self._parse_cloud_data(cloud_data=cloud_data)

    @staticmethod
    def _parse_cloud_data(cloud_data: dict) -> list:
        data = []
        for item in cloud_data:
            timestamp = item.get("timestamp").__int__()
            occupied = 1 if item.get("room_occupied") else 0
            entry = {"timestamp": timestamp, "room_occupied": occupied}
            data.append(entry)
        return data
