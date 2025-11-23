Session Intent Classification & Browsing Behavior Visualization

This project analyzes user web browsing history, groups visits into meaningful sessions, assigns weak intent labels using domain and keyword based heuristics, 
and visualizes behavioral insights. The system also prepares session-level features for downstream machine learning models such as Logistic Regression for intent prediction. An interactive dashboard (in progress) enables real-time exploration of user search patterns.

📌 Project Objectives
Collect and preprocess raw browsing history from CSV input.
Perform sessionization (fixed 1-hour windows).
Categorize visits into six intents:
Education/Career, Social/Entertainment, Shopping, Finance, Travel, General Search, Miscellaneous
Generate session-level summaries and dominant categories.
Perform Exploratory Data Analysis (EDA) with multiple visual insights.
Prepare features for predictive modeling.
Build an interactive dashboard for real-time analytics.

🏗️ Architecture
Data Collection → Pre-processing → Sessionization
          → Weak Labeling → Feature Extraction
          → EDA & Insights → Model Training (In Progress)
          → Dashboard Visualization

📂 Project Structure
📁 project-root
│
├── data/
│   └── user_history.csv
│
├── src/
│   ├── data_collection.py
│   ├── sessionization.py
│   ├── exploratory_data_analysis.py
│   ├── feature_extraction.py (coming soon)
│   └── model_training.py (planned)
│
├── notebooks/
│   └── analysis.ipynb
│
├── README.md
└── requirements.txt

⚙️ Installation & Setup
1️⃣ Clone the repository
git clone https://github.com/<your-username>/<your-repo>.git
cd <your-repo>

2️⃣ Install dependencies
pip install -r requirements.txt

3️⃣ Prepare browsing data

Place your formatted CSV file inside data/ folder:

Required columns:

visit_time

url

title (optional)

user

🚀 Usage
Run Sessionization
from src.sessionization import Sessionization
from src.data_collection import DataCollection

df = DataCollection.final_data()
sessions = Sessionization()
session_df = sessions.sessionization(df)

Run EDA
from src.exploratory_data_analysis import run_eda
run_eda(session_df)

📊 Key EDA Visualizations

The system generates multiple insights, including:

Distribution of dominant categories

Hourly activity heatmap

Session duration vs number of visits

Top visited domains

Category proportions per session

Temporal browsing patterns

These insights validate labeling quality and reveal real browsing behavior trends.

🤖 Weak Labeling (Heuristic + Keyword-Based)

Intent labels are automatically assigned using:

✔ Domain parsing (urlparse)
✔ Search query extraction (q, query, p)
✔ Keyword patterns for each category
✔ Domain-to-category lookup map
✔ Refinement based on EDA corrections

🔮 Future Work

Feature extraction for session-based ML models

Logistic Regression classifier training

Evaluation metrics (Accuracy, F1-score, Confusion Matrix)

Real-time dashboard (Plotly Dash / Streamlit)

Enhanced domain categorization using LLM-assisted suggestions
