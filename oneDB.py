import mysql.connector
import subprocess
import time
from datetime import datetime

db_config = {
    'host': '10.0.15.1',
    'user': 'nacer',
    'passwd': 'pwd123PWD123',
    'database': 'drupal'
}

def backup_database():
    filename = f"backup_{datetime.now().strftime('%Y%m%d%H%M%S')}.sql"
    try:
        db = mysql.connector.connect(**db_config)
        print(f"تم الإتصال بقاعدة البيانات: {db_config['database']}")

        with open(filename, 'w') as output_file:
            subprocess.run(['mysqldump', '-h', db_config['host'], '-u', db_config['user'], '-p'+db_config['passwd'], db_config['database']], stdout=output_file)
        print(f"تم النسخ بنجاح: {filename}")

    except mysql.connector.Error as err:
        print(f"خطأ: {err}")
    finally:
        if db.is_connected():
            db.close()
            print("تم إغلاق الإتصال")

while True:
    backup_database()
    print("توقف لـ 12 ساعة...")
    time.sleep(43200)  # 12 ساعة بالثانية
