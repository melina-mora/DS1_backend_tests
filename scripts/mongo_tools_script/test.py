import os
import pymongo
import subprocess
from dotenv import load_dotenv

load_dotenv()
host = os.getenv('HOST')
conn = pymongo.MongoClient(host)
subprocess.run((
                   'mongorestore --host MeliCluster-shard-0/melicluster-shard-00-00-kkqpl.mongodb.net:27017,melicluster-shard-00-01-kkqpl.mongodb.net:27017,melicluster-shard-00-02-kkqpl.mongodb.net:27017 --ssl --username mromera --password wcO9bvMXvXqVcQT1 --authenticationDatabase admin --nsInclude="*.bson" "C:\\Users\\melina.romera\\Documents\\PROJECT\\_automation\\DS1_backend_tests\\tests\data\\backup_dir\\20191016_173736\\TestData"'))
print(conn)
