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


# src/models/ai_engine.py (tambahkan di akhir)
from ..data.vendors import vendors_data

def recommend_vendors(waste_weight_kg, preference="balanced"):
    """
    Rekomendasikan vendor berdasarkan preferensi:
    - 'fast': minimalkan ETA
    - 'cheap': minimalkan harga
    - 'balanced': campuran
    """
    vendors = []
    for v in vendors_data:
        total_price = v["price_per_kg"] * waste_weight_kg
        score = 0
        if preference == "fast":
            score = -v["eta_min"]  # lebih kecil = lebih baik
        elif preference == "cheap":
            score = -total_price
        else:  # balanced
            # Normalisasi & gabungkan
            norm_eta = 1 - (v["eta_min"] / 60)
            norm_price = 1 - (total_price / 50000)
            score = 0.6 * norm_price + 0.4 * norm_eta
        
        vendors.append({
            **v,
            "total_price": total_price,
            "score": score
        })
    
    return sorted(vendors, key=lambda x: x["score"], reverse=True)
