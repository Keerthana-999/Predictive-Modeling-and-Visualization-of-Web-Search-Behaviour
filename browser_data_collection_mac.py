# import sqlite3
# import pandas as pd
# import os
# import datetime
# import shutil

# # Path to Chrome history DB on macOS
# data_path = os.path.expanduser(
#     "~/Library/Application Support/Google/Chrome/Default/History"
# )

# # Copy database to avoid "database is locked" error
# temp_path = "chrome_history_temp_mac"
# shutil.copy2(data_path, temp_path)

# # Connect to the temporary DB
# conn = sqlite3.connect(temp_path)
# cursor = conn.cursor()

# # SQL Query to fetch URL, title, and visit timestamp
# query = """
# SELECT 
#     urls.url, 
#     urls.title, 
#     visits.visit_time
# FROM urls, visits
# WHERE urls.id = visits.url
# ORDER BY visits.visit_time DESC;
# """

# df = pd.read_sql_query(query, conn)

# # Convert Chrome timestamps (microseconds since 1601) to standard datetime
# def chrome_time_to_datetime(chrome_time):
#     if chrome_time:
#         return datetime.datetime(1601, 1, 1) + datetime.timedelta(microseconds=chrome_time)
#     return None

# df["visit_time"] = df["visit_time"].apply(chrome_time_to_datetime)

# # Export to CSV
# df.to_csv("User_browser_data_mac.csv", index=False)

# conn.close()

# print("Browser history successfully exported to User_browser_data_mac.csv")


import sqlite3
import pandas as pd
import os
import datetime
import shutil

# Path to Safari History database
data_path = os.path.expanduser("~/Library/Safari/History.db")

# Copy DB to avoid locking issues
temp_path = "safari_history_temp.db"
shutil.copy2(data_path, temp_path)

# Connect to the copied DB
conn = sqlite3.connect(temp_path)
cursor = conn.cursor()

# SQL Query to fetch URL, title, and visit time
query = """
SELECT 
    history_items.url,
    history_items.title,
    history_visits.visit_time
FROM history_items
JOIN history_visits
ON history_items.id = history_visits.history_item
ORDER BY history_visits.visit_time DESC;
"""

df = pd.read_sql_query(query, conn)

# Safari timestamps = seconds since 2001-01-01
def safari_time_to_datetime(safari_time):
    if safari_time:
        return datetime.datetime(2001, 1, 1) + datetime.timedelta(seconds=safari_time)
    return None

df["visit_time"] = df["visit_time"].apply(safari_time_to_datetime)

# Export to CSV
df.to_csv("Safari_browser_history.csv", index=False)

conn.close()

print("Safari history successfully exported to Safari_browser_history.csv")
