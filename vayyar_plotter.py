from pathlib import Path
from dataclasses import dataclass

from threading import Thread

from live_plotter import LivePlotter
from post_plotter import PostPlotter


@dataclass(unsafe_hash=True)
class Config:
    live_monitor: bool = False
    weldcloud_overlay: bool = False
    weldcloud_data: Path = Path("data/weldcloud_overlay.xlsx")
    manual_overlay: bool = False
    manaul_data: Path = Path("data/manual_overlay_short.xlsx")

    def __post_init__(self):
        self.post_plotter: bool = self.manual_overlay or self.weldcloud_overlay
        counter = 0
        for overlay in [self.weldcloud_overlay, self.manual_overlay, self.post_plotter]:
            if overlay:
                counter += 1
        self.overlay_counter = counter


if __name__ == '__main__':
    config = Config(live_monitor=False, weldcloud_overlay=False, manual_overlay=True)

    threads = []
    for plotter in [LivePlotter, PostPlotter]:
        thread = Thread(target=plotter, args=(config,))
        threads.append(thread)

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()
