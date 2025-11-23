import pandas as pd
import numpy as np
from urllib.parse import urlparse
from collections import Counter
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix
import warnings
warnings.filterwarnings("ignore")

# -----------------------------
# CONFIG: input files (extendable)
# -----------------------------
user_files = {
    "user_1": "./User_1.csv",
    # "user_2": "./User_2.csv"
    # add more: "user_3": "./user3.csv", ...
}

# -----------------------------
# Helper: load and normalize data
# -----------------------------

class DataCollection:
    def load_and_prep(path, user_label):
        df = pd.read_csv(path)
        # Ensure visit_time exists and parse
        if 'visit_time' not in df.columns:
            raise ValueError(f"File {path} lacks 'visit_time' column.")
        df = df.copy()
        df['visit_time'] = pd.to_datetime(df['visit_time'])
        df['user'] = user_label
        # extract domain safely
        df['domain'] = df['url'].apply(lambda x: urlparse(str(x)).netloc if pd.notnull(x) else None)
        return df

# -----------------------------
# Load all users
# -----------------------------
    def final_data():
        dfs = []
        for user_label, path in user_files.items():
            dfs.append(DataCollection.load_and_prep(path, user_label))
        df = pd.concat(dfs, ignore_index=True)
        df = df.sort_values(['user', 'visit_time']).reset_index(drop=True)
        return df
    
