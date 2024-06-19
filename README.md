# datatemper

Data center temperature monitor for Raspberry Pi with Raspian lite buster and sensor DHT22

Inspired from this project: https://github.com/Mjrovai/RPI-Flask-SQLite

### Dependencies
Python library to read the DHT: https://github.com/adafruit/Adafruit_Python_DHT

### Installation
Install packages
```sh
sudo apt-get install python3-full python3-setuptools python3-setuptools-git python3-seaborn python3-flask python3-rpi.gpio python3-dev python3-matplotlib python3-pip python3-waitress sqlite3 
```

Install Adafruit library
```sh
sudo pip3 install Adafruit_DHT
```

Clone the repository data temper in your working directory (i.e. /opt/apps/) and execute with sudo and testing it
```sh
git clone https://github.com/tomvitale/datatemper.git
cd datatemper
sudo -b python3 datatemper-log.py
sudo -b python3 datatemper.py
```

Connect to http://localhost

### Testing Database
Connect using sqlite3 to database and run some test
```sql
sqlite3 datatemper-data.db
...
## num entries
sqlite> select COUNT(*) from  DHT_data;
...
## display last 10 entries
sqlite> SELECT * FROM DHT_data ORDER BY timestamp DESC LIMIT 10;
...
## display all entries
sqlite> SELECT * FROM DHT_data;
...
## exit
sqlite> .quit
```

You can also delete all entries
```sql
sqlite3 datatemper-data.db
...
sqlite> DELETE FROM DHT_data;
sqlite> .quit
```
### Screenshot
![alt Screenshot](https://raw.githubusercontent.com/tomvitale/datatemper/master/screenshot.png)
