## Peking Educational District in China VS housing prices -- scrapping from fangtianxia

## Python libraries:
   - Install Python3 and pip3
   - pip3 install beautifulsoup4
   - pip3 install requests
   - pip3 install lxml
   - pip3 install pymongo

## Install Mongodb on MAC 
   - brew install mongodb
   - mkdir -p /data/db (set the database path, you choose the location)

## Start Mongod
   - mongod --dbpath <path to data directory>
   - e.g. mongod --dbpath /data/db

## Run the script
   - python3 beijing_haidian.py
   - python3 beijing_dongcheng.py
   - python3 beijing_xicheng.py
   
## How to export database data
   - mongoexport -h localhost:27017 -d beijing_xicheng -c test -o xicheng.json
   - mongoexport -h localhost:27017 -d beijing_xicheng -c test -o xicheng.csv

