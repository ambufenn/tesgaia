# src/config.py
TOKEN_RATE = {
    "plastic": 10,
    "paper": 8,
    "metal": 15,
    "glass": 6,
    "e-waste": 20,
    "mixed": 5
}

WASTE_TYPES = list(TOKEN_RATE.keys())
