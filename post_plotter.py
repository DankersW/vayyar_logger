from typing import Tuple
from datetime import datetime
from dataclasses import dataclass
from time import time

from matplotlib import pyplot

from vayyar_overlay import VayyarOverlay
from weldcloud_overlay import WeldcloudOverlay


class PostPlotter:
    def __init__(self, config: dataclass):
        self.overlays = []
        if config.weldcloud_overlay:
            wc_overlay = WeldcloudOverlay(filename=config.weldcloud_data)
            self.overlays.append(wc_overlay.get_overlay_data())

        if config.post_plotter:
            min_ts, max_ts = self.get_min_max_timestamp()
            vayyay_overlay = VayyarOverlay(min_ts, max_ts)
            self.overlays.append(vayyay_overlay.get_overlay_data())
            self.plot_data(config.overlay_counter)

    def get_min_max_timestamp(self, config: dataclass) -> (int, int):
        if len(self.overlays) == 0:
            return round(time() * 1000), round(time() * 1000) - 86400000

        min_ts = round(time() * 1000)
        max_ts = 0
        for item in self.overlays:
            if item.get("min") < min_ts:
                min_ts = item.get("min")
            if item.get("max") > max_ts:
                max_ts = item.get("max")
        return min_ts, max_ts

    def plot_data(self, overlay_count: int):
        fig = pyplot.figure()
        combined = fig.add_subplot(overlay_count+1, 1, 1)
        for i, overlay in enumerate(self.overlays):
            sub_plot = fig.add_subplot(overlay_count+1, 1, i+2)
            x, y = self._get_plot_data(data=overlay.get("data"))
            sub_plot.step(x, y, label=overlay.get("label"), color=overlay.get("color"))
            combined.step(x, y, label=overlay.get("label"), color=overlay.get("color"))
            sub_plot.legend()
        combined.legend()
        pyplot.show()

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

    @staticmethod
    def _decimal_timestamp_to_dt(timestamp: int) -> datetime:
        return datetime.fromtimestamp(timestamp / 1000)
