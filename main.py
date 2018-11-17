# codeing = utf-8

import Adafruit_DHT as dht
import time
from datetime import datetime
from influxdb import InfluxDBClient
from db_parameter import LOGIN


class Pi(object):
    """
    SENSER: DHT模块的型号，这里使用DHT22
    PIN: GPIO编号
    """
    SENSER = 22
    PIN = 4

    @classmethod
    def get_data(cls):
        """
        获取温度和湿度
        :return: 返回包含温湿度的字典用于后面调用
        """
        humidity, temperature = dht.read_retry(cls.SENSER, cls.PIN)
        return {'temperature': temperature, 'humidity': humidity}

    @staticmethod
    def write_db(data_dict):
        """
        将温湿度参数以及时间戳数据写入InfluxDB中
        :param data_dict: 将温湿度数据的字典传入方法
        :return: 返回写入InfluxDB的结果
        """

        localtime = time.ctime()
        # time为InfluxDB Table中的时间戳

        client = InfluxDBClient(LOGIN['host'], LOGIN['port'],
                                LOGIN['username'], LOGIN['password'], LOGIN['db_name'])
        # client为连接InfluxDB的方法
        data = [
            {
                'measurement': 'dht22-data',
                # 表名为dht22-data
                'tags': {
                    'location': 'Shanghai',
                },
                'time': localtime,
                'fields': {
                    # fields为dht22-data表中的列参数，这里分别存放温度和湿度参数
                    'temperature': data_dict['temperature'],
                    'humidity': data_dict['humidity']
                }
            }

        ]

        client.write_points(data)


if __name__ == '__main__':
    run = Pi()
    interval = 60
    # 每隔60s获取一次数据并写入数据库
    try:
        while True:
            data_res = run.get_data()
            run.write_db(data_res)
            time.sleep(interval)
    except KeyboardInterrupt:
        exit(0)

