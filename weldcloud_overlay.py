from typing import Tuple
from datetime import datetime
from pathlib import Path

from yaml import safe_load
from matplotlib import pyplot
import openpyxl

from db_driver import DbDriver


class WeldcloudOverlay:
    row_first_data = 7
    col_event_created = 2
    col_arc_time = 3

    def __init__(self, filename: Path):
        self.db_room = DbDriver(keys=self._get_keys(), table='vayyar_home_c2c_room_status')
        self.weldcloud_data = self.parse_weldcloud_data(file=filename)
        min_ts, max_ts = self.get_min_max_timestamp()
        self.vayyar_data = self.get_room_data(youngest_ts=min_ts, oldest_ts=max_ts)
        self.plot_data()

    def parse_weldcloud_data(self, file: Path) -> list:
        xlsx = openpyxl.load_workbook(file).active
        data = []
        for row in range(self.row_first_data, xlsx.max_row):
            start_timestamp = xlsx.cell(row=row, column=self.col_event_created, value=None).value
            arc_time = xlsx.cell(row=row, column=self.col_arc_time, value=None).value
            duration = self._arc_time_to_millisec(arc_time)
            data_enty = self._construct_data_entry(start_timestamp=int(start_timestamp), duration=duration)
            data.extend(data_enty)
        return data

    def get_min_max_timestamp(self) -> Tuple[int, int]:
        min_ts = self.weldcloud_data[0].get("timestamp")
        max_ts = self.weldcloud_data[-1].get("timestamp")
        return min_ts, max_ts

    def get_room_data(self, oldest_ts, youngest_ts) -> list:
        cloud_data = self.db_room.query_db(oldest_timestamp=oldest_ts, untill_timestamp=youngest_ts)
        return self._parse_cloud_data(cloud_data=cloud_data)

    def plot_data(self):
        weldcloud_x, weldcloud_y = self._get_plot_data(data=self.weldcloud_data)
        vayyar_x, vayyar_y = self._get_plot_data(data=self.vayyar_data)

        fig = pyplot.figure()
        together = fig.add_subplot(3, 1, 1)
        weldcloud = fig.add_subplot(3, 1, 2)
        vayyar = fig.add_subplot(3, 1, 3)

        together.step(vayyar_x, vayyar_y, label="vayyar", color="orange")
        together.step(weldcloud_x, weldcloud_y, label="weldcloud", color="green")

        vayyar.step(vayyar_x, vayyar_y, label="vayyar", color="orange")
        weldcloud.step(weldcloud_x, weldcloud_y, label="weldcloud", color="green")

        together.legend()
        vayyar.legend()
        weldcloud.legend()
        pyplot.show()

    @staticmethod
    def _get_keys():
        with open("keys.yml") as config_file:
            return safe_load(config_file)

    @staticmethod
    def _arc_time_to_millisec(arc_time: str) -> int:
        time_values = arc_time.split(sep=' ')
        duration = 0
        if any("minute" in time_value for time_value in time_values):
            duration += int(time_values[0]) * 60000
        if any("second" in time_value for time_value in time_values):
            duration += int(time_values[-2]) * 1000
        return duration

    @staticmethod
    def _construct_data_entry(start_timestamp: int, duration: int) -> list:
        data = []
        if duration != 0:
            data = [{"timestamp": start_timestamp - 1, "welding": 0},
                    {"timestamp": start_timestamp, "welding": 1},
                    {"timestamp": start_timestamp + duration, "welding": 1},
                    {"timestamp": start_timestamp + duration + 1, "welding": 0}]
        return data

    @staticmethod
    def _decimal_timestamp_to_dt(timestamp: int) -> datetime:
        return datetime.fromtimestamp(timestamp / 1000)

    @staticmethod
    def _parse_cloud_data(cloud_data: dict) -> list:
        data = []
        for item in cloud_data:
            timestamp = item.get("timestamp").__int__()
            occupied = 1 if item.get("room_occupied") else 0
            entry = {"timestamp": timestamp, "room_occupied": occupied}
            data.append(entry)
        return data

    def _get_plot_data(self, data: list) -> Tuple[list, list]:
        x = []
        y = []
        for item in data:
            _x = self._decimal_timestamp_to_dt(item.get("timestamp"))
            if "welding" in item:
                _y = item.get("welding")
            else:
                _y = item.get("room_occupied")
            x.append(_x)
            y.append(_y)
        return x, y


if __name__ == '__main__':
    filepath = Path("data/Weldcloud_Export_Weldsessions.xlsx")
    WeldcloudOverlay(filename=filepath)
