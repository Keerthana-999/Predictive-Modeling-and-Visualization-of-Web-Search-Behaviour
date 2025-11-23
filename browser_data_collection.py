import sqlite3
import pandas as pd
import os
import datetime
import shutil

data_path = os.path.expanduser(
    r"~\AppData\Local\Google\Chrome\User Data\Default\History"
)

temp_path = "chrome_history_temp"
shutil.copy2(data_path, temp_path)


conn = sqlite3.connect(temp_path)
cursor = conn.cursor()


query = """
SELECT 
    urls.url, 
    urls.title, 
    visits.visit_time
FROM urls, visits
WHERE urls.id = visits.url
ORDER BY visits.visit_time DESC;
"""

df = pd.read_sql_query(query, conn)

def chrome_time_to_datetime(chrome_time):
    return datetime.datetime(1601, 1, 1) + datetime.timedelta(microseconds=chrome_time)

df["visit_time"] = df["visit_time"].apply(chrome_time_to_datetime)
df.to_csv('User_browser_data.csv')
conn.close()