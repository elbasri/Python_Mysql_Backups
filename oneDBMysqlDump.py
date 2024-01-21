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
        with open(filename, 'w') as output_file:
            subprocess.run(['mysqldump', '-h', db_config['host'], '-u', db_config['user'], '-p'+db_config['passwd'], db_config['database']], stdout=output_file)
        print(f"تم النسخ بنجاح: {filename}")

    except Exception as err:
        print(f"خطأ: {err}")

while True:
    backup_database()
    print("توقف لـ 12 ساعة...")
    time.sleep(43200)  # 12 ساعة بالثانية
