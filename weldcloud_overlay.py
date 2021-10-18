import openpyxl
from pathlib import Path


class WeldcloudOverlay:
    row_first_data = 7
    col_event_created = 2
    col_arc_time = 3

    def __init__(self, filename: Path):
        self.data = self.parse_weldcloud_data(file=filename)

    def parse_weldcloud_data(self, file: Path) -> list:
        xlsx = openpyxl.load_workbook(file).active
        data = []
        for row in range(self.row_first_data, xlsx.max_row):
            start_timestamp = xlsx.cell(row=row, column=self.col_event_created, value=None).value
            arc_time = xlsx.cell(row=row, column=self.col_arc_time, value=None).value
            duration = self.arc_time_to_millisec(arc_time)
            data_enty = self.construct_data_entry(start_timestamp=int(start_timestamp), duration=duration)
            data.extend(data_enty)
        return data

    @staticmethod
    def arc_time_to_millisec(arc_time: str) -> int:
        time_values = arc_time.split(sep=' ')
        duration = 0
        if any("minute" in time_value for time_value in time_values):
            duration += int(time_values[0]) * 60000
        if any("second" in time_value for time_value in time_values):
            duration += int(time_values[-2]) * 1000
        return duration

    @staticmethod
    def construct_data_entry(start_timestamp: int, duration: int) -> list:
        data = []
        if duration != 0:
            data = [{"timestamp": start_timestamp, "welding": 1}, {"timestamp": start_timestamp + duration, "welding": 0}]
        return data

if __name__ == '__main__':
    parse_weldcloud_csv()
    filepath = Path("data/Weldcloud_Export_Weldsessions.xlsx")
    WeldcloudOverlay(filename=filepath)
