import matplotlib.pyplot as plt
import seaborn as sns
from sessionization import Sessionization
from data_collection import DataCollection

# -----------------------------
# EDA: multiple plots and insights
# -----------------------------
sns.set(style="whitegrid")
df = DataCollection.final_data()
session_df = Sessionization.sessionization(df)
# 1. Count of dominant categories
plt.figure(figsize=(10,5))
order = session_df['dominant_category'].value_counts().index
sns.countplot(x='dominant_category', data=session_df, order=order, palette='tab10')
plt.title("Distribution of Dominant Categories per 1-hour Session")
plt.xlabel("Dominant Category")
plt.ylabel("Session Count")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# 2. Category share pie chart
plt.figure(figsize=(6,6))
counts = session_df['dominant_category'].value_counts()
plt.pie(counts, labels=counts.index, autopct='%1.1f%%', startangle=140)
plt.title("Category Share Across Sessions")
plt.tight_layout()
plt.show()

# 3. Session duration (observed span) by category (boxplot)
plt.figure(figsize=(10,5))
sns.boxplot(x='dominant_category', y='duration_minutes_observed', data=session_df, order=order)
plt.title("Observed Session Span (minutes) by Dominant Category")
plt.xlabel("Dominant Category")
plt.ylabel("Observed Span (minutes)")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# 4. Number of visits by category (boxplot)
plt.figure(figsize=(10,5))
sns.boxplot(x='dominant_category', y='num_visits', data=session_df, order=order)
plt.title("Number of Visits per Session by Dominant Category")
plt.xlabel("Dominant Category")
plt.ylabel("Number of Visits")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# 5. Correlation heatmap of numeric features
numeric_cols = ['num_visits', 'unique_domains', 'duration_minutes_observed', 'duration_minutes']
corr_df = session_df[numeric_cols].corr()
plt.figure(figsize=(7,5))
sns.heatmap(corr_df, annot=True, fmt=".2f", cmap='Blues')
plt.title("Correlation of Numeric Session Features")
plt.tight_layout()
plt.show()

# 6. Hourly activity pattern
session_df['hour'] = session_df['session_start'].dt.hour
plt.figure(figsize=(12,4))
sns.countplot(x='hour', data=session_df, palette='crest')
plt.title("Sessions per Hour of Day")
plt.xlabel("Hour")
plt.ylabel("Number of Sessions")
plt.tight_layout()
plt.show()

# 7. Weekly pattern
session_df['weekday'] = session_df['session_start'].dt.day_name()
order_week = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
plt.figure(figsize=(12,4))
sns.countplot(x='weekday', data=session_df, order=order_week, palette='Spectral')
plt.title("Sessions per Day of Week")
plt.xlabel("Day of Week")
plt.ylabel("Number of Sessions")
plt.tight_layout()
plt.show()

# 8. Top domains overall
top_domains = df['domain'].value_counts().head(20)
plt.figure(figsize=(10,6))
sns.barplot(x=top_domains.values, y=top_domains.index, palette='mako')
plt.title("Top 20 Visited Domains")
plt.xlabel("Visit Count")
plt.ylabel("Domain")
plt.tight_layout()
plt.show()

# 9. Avg unique domains per session by category
avg_unique = session_df.groupby('dominant_category')['unique_domains'].mean().sort_values(ascending=False)
plt.figure(figsize=(8,4))
sns.barplot(x=avg_unique.values, y=avg_unique.index, palette='viridis')
plt.title("Average Unique Domains per Session by Category")
plt.xlabel("Avg Unique Domains")
plt.ylabel("Category")
plt.tight_layout()
plt.show()

# 10. Hour vs Category heatmap
hour_cat = session_df.groupby(['hour','dominant_category']).size().unstack(fill_value=0)
plt.figure(figsize=(12,6))
sns.heatmap(hour_cat, cmap='YlGnBu')
plt.title("Heatmap: Hour of Day vs Dominant Category")
plt.xlabel("Category")
plt.ylabel("Hour")
plt.tight_layout()
plt.show()

# 11. Duration vs visits scatter
plt.figure(figsize=(8,6))
sns.scatterplot(x='num_visits', y='duration_minutes_observed', hue='dominant_category', data=session_df, alpha=0.7)
plt.title("Observed Duration vs Number of Visits (colored by category)")
plt.xlabel("Number of Visits")
plt.ylabel("Observed Duration (minutes)")
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.show()

# 12. Category composition per user (stacked counts)
plt.figure(figsize=(10,6))
sns.countplot(x='user', hue='dominant_category', data=session_df, palette='Set3')
plt.title("Category Counts per User")
plt.xlabel("User")
plt.ylabel("Number of Sessions")
plt.legend(title='Category', bbox_to_anchor=(1.05,1))
plt.tight_layout()
plt.show()