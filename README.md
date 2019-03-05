# datatemper

Data center temperature monitor for Raspberry Pi and sensor DHT22

### Dependencies
Python library to read the DHT: https://github.com/adafruit/Adafruit_Python_DHT

### Installation
Install packages
```sh
$ sudo apt-get install python3-setuptools python3-setuptools-git python3-seaborn python3-flask python3-rpi.gpio python3.5-dev python3-matplotlib sqlite3
```

Clone the repository Adafruit and compile it
```sh
$ git clone https://github.com/adafruit/Adafruit_Python_DHT.git
$ cd Adafruit_Python_DHT
$ sudo python3.5 setup.py install
```

Clone the repository data temper in your working directory (i.e. /opt/apps/) and execute with sudo and testing it
```sh
$ git clone https://github.com/adafruit/Adafruit_Python_DHT.git
$ cd datatemper
$ sudo python3.5 datatemper-log.py &
$ sudo python3.5 datatemper.py &
```

Connect to http://localhost

### Testing Database
Connect using sqlite3 to database and run some test
```sql
$ sqlite3 datatemper-data.db
...
## num entries
sqlite> select COUNT(*) from  DHT_data;
...
## display last 10 entries
sqlite> SELECT * FROM DHT_data ORDER BY timestamp DESC LIMIT 10;
...
## display all entries
sqlite> SELECT * FROM DHT_DATA;
...
## exit
sqlite> .quit
```

You can also delete all entries
```sql
$ sqlite3 datatemper-data.db
...
sqlite> DELETE FROM DHT_DATA;
sqlite> .quit
```
