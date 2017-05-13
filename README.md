## Peking Educational District in China VS housing prices -- scraping from fangtianxia
   - Scrape data from one of the largest second-hand housing resource websites
   - [fangtianxia](http://www.fang.com/)

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


## How to coordinate transform Map lat/lon for Baidu.com
   - The geo info from Fangtianxia is from Baidu, which has its own lat/lon code. 
   - coordTransform_utils.py allow you transform the lat/lon for those from baidu map API.
   - e.g. python coordTransform_utils.py data-cleaned/court/dongcheng_xiaoqu_cleaned.csv OutPutFileName.csv
