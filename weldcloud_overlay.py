import openpyxl
from pathlib import Path


def arc_time_to_millisec(arc_time: str) -> int:
    time_values = arc_time.split(sep=' ')
    duration = 0
    if any("minute" in time_value for time_value in time_values):
        duration += int(time_values[0]) * 60000
    if any("second" in time_value for time_value in time_values):
        duration += int(time_values[-2]) * 1000
    return duration


def construct_data_entry(start_timestamp: int, duration: int) -> list:
    data = []
    if duration != 0:
        data = [{"timestamp": start_timestamp, "welding": 1}, {"timestamp": start_timestamp + duration, "welding": 0}]
    return data

def parse_weldcloud_csv():
    filename = Path("data/Weldcloud_Export_Weldsessions.xlsx")
    xlsx = openpyxl.load_workbook(filename=filename).active
    row_first_data = 7
    column_event_created = 2
    column_arc_time = 3

    # Iterate the loop to read the cell values
    data = []
    for row in range(row_first_data, xlsx.max_row):
        start_timestamp = xlsx.cell(row=row, column=column_event_created, value=None).value
        arc_time = xlsx.cell(row=row, column=column_arc_time, value=None).value
        print(start_timestamp, arc_time)

        duration = arc_time_to_millisec(arc_time)
        data_enty = construct_data_entry(start_timestamp=int(start_timestamp), duration=duration)
        data.extend(data_enty)
    print(data)



if __name__ == '__main__':
    parse_weldcloud_csv()
