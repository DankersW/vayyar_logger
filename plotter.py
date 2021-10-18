from pathlib import Path

from live_plotter import LivePlotter
from weldcloud_overlay import WeldcloudOverlay

if __name__ == '__main__':
    weldcloud_data = Path("data/Weldcloud_Export_Weldsessions.xlsx")

    #LivePlotter()
    WeldcloudOverlay(filename=weldcloud_data)
