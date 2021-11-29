from pathlib import Path
from dataclasses import dataclass

from live_plotter import LivePlotter
from weldcloud_overlay import WeldcloudOverlay


@dataclass(unsafe_hash=True)
class Config:
    live_monitor: bool = False
    weldcloud_overlay: bool = False
    weldcloud_data: Path = Path("data/Weldcloud_overlay.xlsx")
    manual_overlay: bool = False
    manaul_data: Path = Path("data/manual_overlay.xlsx")


if __name__ == '__main__':

    config = Config(live_monitor=False, weldcloud_overlay=True, manual_overlay=True)
    print(config)

    live_thread = Thr

    #weldcloud_data = Path()

    #LivePlotter()
    #WeldcloudOverlay(filename=weldcloud_data)
