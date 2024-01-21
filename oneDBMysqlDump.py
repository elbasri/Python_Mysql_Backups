# سكريبت يستخدم mysqldump لأخذ نسخة احتياطية من قاعدة بيانات محددة كل 12 ساعة

import subprocess
import time
from datetime import datetime
from config import db_config  # استيراد بيانات الاتصال من ملف config.py

def backup_database():
    filename = f"../files/backup_{datetime.now().strftime('%Y%m%d%H%M%S')}.sql"
    try:
        # تنفيذ أمر mysqldump لأخذ النسخة الاحتياطية
        with open(filename, 'w') as output_file:
            subprocess.run(['mysqldump', '-h', db_config['host'], '-u', db_config['user'], '-p'+db_config['passwd'], db_config['database']], stdout=output_file)
        print(f"تم النسخ بنجاح: {filename}")

    except Exception as err:
        print(f"خطأ: {err}")

# حلقة لتشغيل النسخ الاحتياطي كل 12 ساعة
while True:
    backup_database()
    print("توقف لـ 12 ساعة...")
    time.sleep(43200)  # 12 ساعة بالثانية
