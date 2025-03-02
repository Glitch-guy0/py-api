from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError


try:
  _dbClient = MongoClient("mongodb://localhost:27017/", maxPoolSize=50, minPoolSize=10, maxIdleTimeMS=10000, serverSelectionTimeoutMS=5000)
  _dbClient.server_info()
except ServerSelectionTimeoutError as connErr:
  print("Cannot Connect to DB! Check if it's running!")
except Exception as e:
  print(e)

## Collections
## Service
User = _dbClient["py-api"]["users"]

## gateway
Blocklist = {
  "Session": _dbClient["py-api"]["session_blocklist"],
  "IP": _dbClient["py-api"]["ip_blocklist"]
}

Log = {
  "IP": _dbClient["py-api"]["ip_log"]
}