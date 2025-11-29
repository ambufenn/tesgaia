# src/core/blockchain.py
import hashlib
from datetime import datetime
from typing import Any, Dict, List

class Wallet:
    def __init__(self):
        self.green_coin = 0
        self.eth = 0.01  # gas balance

    def to_dict(self):
        return {"GreenCoin": self.green_coin, "ETH": self.eth}

class Blockchain:
    def __init__(self):
        self.chain: List[Dict] = []
        self.requests: List[Dict] = []

    def add_block(self, data: Dict[str, Any]):
        prev_hash = self.chain[-1]["hash"] if self.chain else "0" * 64
        block = {
            "index": len(self.chain),
            "timestamp": datetime.now().isoformat(),
            "data": data,
            "prev_hash": prev_hash,
            "hash": hashlib.sha256((str(data) + prev_hash).encode()).hexdigest()
        }
        self.chain.append(block)

    def get_last_blocks(self, n=3):
        return self.chain[-n:][::-1]
