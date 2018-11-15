# PiEnv-Monitor
## 功能
- 使用树莓派采集环境温度将数据存放InfluxDB，Grafana读取数据并输出图表<br>
![](/Pictures/Final%20Grafana.png)

## 平台
- 树莓派3B+，DHT22温湿度传感器<br>
- InfluxDB以及Grafana均安装在CentOS 7.5
#### 1 配置InfluxDB
```sql
create database "data"
create user "admin" with password "influxadmin"
grant all privileges to admin
```
#### 2 配置Grafana
- 增加InfluxDB数据源<br>
![](/Pictures/DataSources.jpg)
- 创建Dashboard<br>
![](/Pictures/Create-Dashboard.jpg)
- 添加并编辑Panel<br>
![](/Pictures/Graph.jpg)

