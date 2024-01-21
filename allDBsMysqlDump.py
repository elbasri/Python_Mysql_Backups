# سكريبت لأخذ نسخ احتياطية من جميع قواعد البيانات على الخادم باستثناء القواعد النظامية

import subprocess
import os
from datetime import datetime
from config import db_config  # استيراد بيانات الاتصال من ملف config.py

DB_HOST = db_config['host']
DB_USER = db_config['user']
DB_PASSWORD = db_config['passwd']

# مسار حفظ النسخ الاحتياطية - تغييره حسب النظام
BACKUP_DIR = r"C:\backups\files"  # ويندوز
# BACKUP_DIR = "/home/backups/files"  # لينكس

TIMESTAMP = datetime.now().strftime("%Y%m%d-%H%M%S")

# التأكد من وجود مجلد النسخ الاحتياطية
if not os.path.exists(BACKUP_DIR):
    os.makedirs(BACKUP_DIR)

# الحصول على قائمة قواعد البيانات
list_databases_cmd = ["mysql", "-h", DB_HOST, "-u", DB_USER, "-p" + DB_PASSWORD, "-e", "SHOW DATABASES"]
result = subprocess.run(list_databases_cmd, stdout=subprocess.PIPE, text=True, check=True)
databases = result.stdout.strip().split('\n')[1:]

for database in databases:
    database = database.strip()
    print(f"جاري العمل على القاعدة: {database}")
    if database not in ["information_schema", "performance_schema", "mysql", "sys"]:
        backup_file = os.path.join(BACKUP_DIR, f"{database}_{TIMESTAMP}.sql")
        
        # تكوين أمر mysqldump لكل قاعدة بيانات
        mysqldump_cmd = ["mysqldump", "-h", DB_HOST, "-u", DB_USER, "-p" + DB_PASSWORD, "--databases", database, "--result-file", backup_file]

        try:
            subprocess.run(mysqldump_cmd, check=True)
            print(f"تم إنشاء نسخة من القاعدة: {database}")
        except subprocess.CalledProcessError as e:
            print(f"هناك مشكلة في القاعدة: {database}: {e}")
