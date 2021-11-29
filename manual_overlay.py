from pathlib import Path
import openpyxl


class ManualOverlay:
    def __init__(self, filename: Path):
        self.filename = filename
        self._data = self._parse_data()

    def _parse_data(self) -> list:
        xlsx = openpyxl.load_workbook(self.filename).active
        data = []
        for row in range(xlsx.max_row):
            timestamp = xlsx.cell(row=row+1, column=1, value=None).value
            room_status = xlsx.cell(row=row+1, column=2, value=None).value
            data.append({"timestamp": timestamp, "room_occupied": room_status})
        print(data)
        return data

    def get_overlay_data(self) -> dict:
        data = {"data": self._data, "min": self._data[-1].get("timestamp"), "max": self._data[0].get("timestamp"),
                "label": "manual", "color": "blue"}
        return data
