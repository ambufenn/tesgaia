# src/models/ai_engine.py
import random
from ..config import WASTE_TYPES

def ai_estimate_waste_from_image(uploaded_file) -> tuple[str, float]:
    """
    Simulasi AI Vision: dari file gambar (diupload), estimasi jenis & berat.
    Dalam produksi: ganti dengan model image classifier (misal: Vertex AI).
    """
    # Pilih acak tapi realistis
    waste_type = random.choice(WASTE_TYPES)
    weight = round(random.uniform(0.5, 8.0), 1)
    return waste_type, weight
