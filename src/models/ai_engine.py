# src/models/ai_engine.py
import os
import random
import pandas as pd
from ..config import TOKEN_RATE

# 🔥 Perbaiki path ke data/waste_samples.csv (di ROOT, bukan di src/data)
DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "data", "waste_samples.csv")

# Load dataset dengan aman
try:
    waste_df = pd.read_csv(DATA_PATH)
    WASTE_TYPES = waste_df["waste_type"].tolist()
    AVG_WEIGHTS = dict(zip(waste_df["waste_type"], waste_df["avg_weight_kg"]))
except Exception as e:
    # Fallback jika file tidak ditemukan (misal di Streamlit Cloud)
    WASTE_TYPES = list(TOKEN_RATE.keys())
    AVG_WEIGHTS = {k: 2.5 for k in WASTE_TYPES}

def ai_estimate_waste_from_image(uploaded_file):
    waste_type = random.choice(WASTE_TYPES)
    base_weight = AVG_WEIGHTS.get(waste_type, 2.5)
    weight = round(base_weight + random.uniform(-0.8, 1.2), 1)
    weight = max(0.3, min(10.0, weight))
    return waste_type, weight
