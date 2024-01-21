import subprocess
import os
from datetime import datetime

DB_HOST = "10.0.15.1"
DB_USER = "nacer"
DB_PASSWORD = "pwd123PWD123" 

#ويندوز
BACKUP_DIR = r"C:\backups\\files"
#لينكس
#BACKUP_DIR = "/home/backups/files"

TIMESTAMP = datetime.now().strftime("%Y%m%d-%H%M%S")

mysqldump_cmd = [
    "mysqldump",
    "-h", DB_HOST,
    "-u", DB_USER,
    "-p" + DB_PASSWORD,
]

list_databases_cmd = ["mysql", "-h", DB_HOST, "-u", DB_USER, "-p" + DB_PASSWORD, "-e", "SHOW DATABASES"]
result = subprocess.run(list_databases_cmd, stdout=subprocess.PIPE, text=True, check=True)
databases = result.stdout.strip().split('\n')[1:]

for database in databases:
    print(f"جاري العمل على القاعدة: {database}")
    database = database.strip()
    if database not in ["information_schema", "performance_schema", "mysql", "sys"]:
        backup_file = os.path.join(BACKUP_DIR, f"{database}_{TIMESTAMP}.sql")
        mysqldump_cmd.extend(["--databases", database, "--result-file", backup_file])
        
        try:
            subprocess.run(mysqldump_cmd, check=True)
            print(f"تم إنشاء نسخة من القاعدة : {database}")
        except subprocess.CalledProcessError as e:
            print(f"هناك مشكلة في القاعدة: {database}: {e}")
