```bash
sortsmart-blockchain/
├── app.py                  ← HANYA UI Streamlit (entrypoint)
├── requirements.txt
├── data/
│   └── waste_samples.csv   ← contoh data sampah (CSV)
└── src/
    ├── core/
    │   └── blockchain.py   ← wallet, ledger, transaksi (logika blockchain sederhana)
    ├── models/
    │   └── ai_engine.py    ← mock AI vision (deteksi kategori sampah contoh)
    └── config.py           ← konstanta (TOKEN_RATE, dsb.)
```
