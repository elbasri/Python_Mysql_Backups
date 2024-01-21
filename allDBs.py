# سكريبت لأخذ نسخ احتياطية من جميع قواعد البيانات على الخادم باستثناء القواعد النظامية باستخدام mysql.connector

import mysql.connector
import os
from datetime import datetime
from config import db_config  # استيراد بيانات الاتصال من ملف config.py

# مسار حفظ النسخ الاحتياطية
BACKUP_DIR = r"../files"

TIMESTAMP = datetime.now().strftime("%Y%m%d-%H%M%S")

def backup_database(db_name):
    """ أخذ نسخة احتياطية من قاعدة بيانات محددة """
    conn = mysql.connector.connect(host=db_config['host'], user=db_config['user'], password=db_config['passwd'], database=db_name)
    cursor = conn.cursor()
    cursor.execute("SHOW TABLES")

    for (table_name,) in cursor:
        backup_table(db_name, table_name)

    cursor.close()
    conn.close()

def backup_table(db_name, table_name):
    """ أخذ نسخة احتياطية من جدول محدد """
    backup_file = os.path.join(BACKUP_DIR, f"{db_name}_{table_name}_{TIMESTAMP}.sql")
    conn = mysql.connector.connect(host=db_config['host'], user=db_config['user'], password=db_config['passwd'], database=db_name)
    cursor = conn.cursor()
    query = f"SELECT * INTO OUTFILE '{backup_file}' FROM {table_name}"
    
    try:
        cursor.execute(query)
        print(f"تم إنشاء نسخة من الجدول: {table_name} في قاعدة البيانات: {db_name}")
    except mysql.connector.Error as err:
        print(f"خطأ في الجدول: {table_name}: {err}")
    finally:
        cursor.close()
        conn.close()

# الحصول على قائمة قواعد البيانات
try:
    conn = mysql.connector.connect(host=db_config['host'], user=db_config['user'], password=db_config['passwd'])
    cursor = conn.cursor()
    cursor.execute("SHOW DATABASES")

    for (database,) in cursor:
        database = database.strip()
        if database not in ["information_schema", "performance_schema", "mysql", "sys"]:
            print(f"جاري العمل على القاعدة: {database}")
            backup_database(database)

    cursor.close()
    conn.close()
except mysql.connector.Error as err:
    print(f"خطأ: {err}")
