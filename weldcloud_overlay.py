import openpyxl
from pathlib import Path


def parse_weldcloud_csv():
    filename = Path("data/Weldcloud_Export_Weldsessions.xlsx")
    xlsx = openpyxl.load_workbook(filename=filename).active
    first_data_postition = 6

    # Iterate the loop to read the cell values
    for i in range(first_data_postition, xlsx.max_row):
        for col in xlsx.iter_cols(1, xlsx.max_column):
            print(col[i].value, end="\t\t")
        print('')


if __name__ == '__main__':
    parse_weldcloud_csv()
