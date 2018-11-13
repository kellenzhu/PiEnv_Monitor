# codeing = utf-8

import Adafruit_DHT as dht
from datetime import datetime
from influxdb import InfluxDBClient


class Pi(object):

    SENSER = 22
    PIN = 4

    @classmethod
    def __get_data(cls):
        humidity, temperature = dht.read_retry(cls.SENSER, cls.PIN)
        return {'temperature': temperature, 'humidity': humidity}

    def alarm_count(self):
        data_dict = self.__get_data()
        alarm_count = 0
        if data_dict['temperature'] >= 40 or data_dict['humidity'] >= 80:
            alarm_count = 1

        return alarm_count

    def stdout_data(self):
        data_dict = self.__get_data()
        print("Current Temperature is {0:0.1f}°, humidity is {1:0.1f}%"
              .format(data_dict['temperature'], data_dict['humidity']))

    def write_db(self):
        data_dict = self.__get_data()
        login = {
            'host': '10.60.1.230',
            'port': 8086,
            'username': 'influx',
            'password': 'influx',
            'db_name': 'sensor_data'
        }

        client = InfluxDBClient(login['host'], login['port'],
                                login['username'], login['password'], login['db_name'])

        data = [
            {
                'measurement': 'rpi-dht22',
                'tags': {
                    'location': 'TBI Shanghai DC',
                },
                'time': datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ'),
                'fields': {
                    'temperature': data_dict['temperature'],
                    'humidity': data_dict['humidity']
                }
            }

        ]

        client.write_points(data)


if __name__ == '__main__':
    run = Pi()
    run.write_db()
