import boto3
import matplotlib.pyplot
from boto3.dynamodb.conditions import Key
from yaml import safe_load
import time
from typing import Tuple
from matplotlib import pyplot, dates, animation
import datetime

class DbDriver:
    device_id = 'id_MzA6QUU6QTQ6RTQ6MDA6NTQ'
    def __init__(self, keys: dict, table: str):
        session = boto3.Session(
            aws_access_key_id=keys.get("aws_access_key"),  # named tuple settings
            aws_secret_access_key=keys.get("aws_secret_key"),
        )
        db = session.resource('dynamodb')
        self.db_table = db.Table(table)

    def query_db(self, oldest_timestamp, untill_timestamp=None):
        if untill_timestamp:
            query = Key('device_id').eq(self.device_id) & Key('timestamp').between(oldest_timestamp, untill_timestamp)
        else:
            query = Key('device_id').eq(self.device_id) & Key('timestamp').gte(oldest_timestamp)
            #query = Key('device_id').eq(self.device_id) & Key('timestamp').between(oldest_timestamp, 1626687473931)
        return self.db_table.query(KeyConditionExpression=query)['Items']

    def scan_db(self):
        return self.db_table.scan()['Items']


class Plotter:
    def __init__(self):
        self.db = DbDriver(keys=self._get_keys(), table='vayyar_home_c2c_room_status')

        self.start_timestamp = round(time.time() * 1000)
        #self.start_timestamp = 1626686100002

        fig = pyplot.figure()
        self.live_plot = fig.add_subplot(2, 1, 1)
        self.yesterday_plot = fig.add_subplot(2, 1, 2)

        _ = animation.FuncAnimation(fig, self.plot_live, interval=300000)
        #self.plot_live(None)
        self.plot_yesterday_room_occupation()

        fig.autofmt_xdate()
        pyplot.show()

    @staticmethod
    def _get_keys():
        with open("keys.yml") as config_file:
            return safe_load(config_file)

    def plot_live(self, _):
        data = self.db.query_db(oldest_timestamp=self.start_timestamp)
        self._plot_data(sub_plot=self.live_plot, data=data)

    def plot_yesterday_room_occupation(self):
        timestamp_yesterday = self.start_timestamp - 86400000
        yesterday_data = self.db.query_db(oldest_timestamp=timestamp_yesterday, untill_timestamp=self.start_timestamp)
        self._plot_data(sub_plot=self.yesterday_plot, data=yesterday_data)

    def _plot_data(self, sub_plot: matplotlib.pyplot.subplot, data: list):
        x = []
        y = []
        for item in data:
            dt, room_occupied = self._parse_data_entry(entry=item)
            x.append(dt)
            y.append(room_occupied)

        date_fmt = '%d-%m-%y %H:%M:%S'
        date_formatter = dates.DateFormatter(date_fmt)
        sub_plot.xaxis.set_major_formatter(date_formatter)
        sub_plot.step(x, y)

    @staticmethod
    def _parse_data_entry(entry: dict) -> Tuple[datetime.datetime, int]:
        timestamp = entry.get("timestamp").__int__() / 1000
        dt = datetime.datetime.fromtimestamp(timestamp)
        occupied = 1 if entry.get("room_occupied") else 0
        return dt, occupied

# todo: live plot

if __name__ == '__main__':
    Plotter()
