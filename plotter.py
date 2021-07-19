from yaml import safe_load
from time import time
from datetime import datetime
from typing import Tuple

from matplotlib import pyplot, animation

from db_driver import DbDriver


class Plotter:
    def __init__(self):
        self.db = DbDriver(keys=self._get_keys(), table='vayyar_home_c2c_room_status')

        self.start_timestamp = round(time() * 1000)

        fig = pyplot.figure()
        self.live_plot = fig.add_subplot(2, 1, 1)
        self.yesterday_plot = fig.add_subplot(2, 1, 2)

        _ = animation.FuncAnimation(fig, self.plot_live, interval=60000)
        self.plot_yesterday_room_occupation()

        pyplot.setp(self.live_plot.get_xticklabels(), rotation=30, ha='right')
        pyplot.setp(self.yesterday_plot.get_xticklabels(), rotation=30, ha='right')
        pyplot.show()

    @staticmethod
    def _get_keys():
        with open("keys.yml") as config_file:
            return safe_load(config_file)

    def plot_live(self, _):
        data = self.db.query_db(oldest_timestamp=self.start_timestamp)
        self._plot_data(sub_plot=self.live_plot, data=data)
        self.live_plot.set_title("Live monitoring")

    def plot_yesterday_room_occupation(self):
        timestamp_yesterday = self.start_timestamp - 86400000
        yesterday_data = self.db.query_db(oldest_timestamp=timestamp_yesterday, untill_timestamp=self.start_timestamp)
        self._plot_data(sub_plot=self.yesterday_plot, data=yesterday_data)
        self.yesterday_plot.set_title("Occupance past day")

    def _plot_data(self, sub_plot: pyplot.subplot, data: list):
        x = []
        y = []
        for item in data:
            dt, room_occupied = self._parse_data_entry(entry=item)
            x.append(dt)
            y.append(room_occupied)
        sub_plot.step(x, y)

    @staticmethod
    def _parse_data_entry(entry: dict) -> Tuple[datetime, int]:
        timestamp = entry.get("timestamp").__int__() / 1000
        dt = datetime.fromtimestamp(timestamp)
        occupied = 1 if entry.get("room_occupied") else 0
        return dt, occupied


if __name__ == '__main__':
    Plotter()
