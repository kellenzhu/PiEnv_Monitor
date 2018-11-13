# codeing = utf-8

import Adafruit_DHT as dht
import time
from datetime import datetime
from influxdb import InfluxDBClient
from db_parameter import LOGIN


class Pi(object):

    SENSER = 22
    PIN = 4

    @classmethod
    def get_data(cls):
        humidity, temperature = dht.read_retry(cls.SENSER, cls.PIN)
        return {'temperature': temperature, 'humidity': humidity}

    @staticmethod
    def alarm_count(data_dict):
        alarm_count = 0
        if data_dict['temperature'] >= 40 or data_dict['humidity'] >= 80:
            alarm_count = 1

        return alarm_count

    @staticmethod
    def stdout_data(data_dict):
        print("Current Temperature is {0:0.1f}°, humidity is {1:0.1f}%"
              .format(data_dict['temperature'], data_dict['humidity']))

    @staticmethod
    def write_db(data_dict):

        time = datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')
        client = InfluxDBClient(LOGIN['host'], LOGIN['port'],
                                LOGIN['username'], LOGIN['password'], LOGIN['db_name'])
        data = [
            {
                'measurement': 'rpi-dht22',
                'tags': {
                    'location': 'TBI Shanghai DC',
                },
                'time': time,
                'fields': {
                    'temperature': data_dict['temperature'],
                    'humidity': data_dict['humidity']
                }
            }

        ]

        client.write_points(data)


if __name__ == '__main__':
    run = Pi()
    interval = 60
    try:
        while True:
            data_res = run.get_data()
            run.write_db(data_res)
            time.sleep(interval)
    except KeyboardInterrupt:
        exit(0)

