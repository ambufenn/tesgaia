import streamlit as st
import pandas as pd
import hashlib
import time
from datetime import datetime

# ====== CONFIG ======
st.set_page_config(page_title="SortSmart – Blockchain Waste Ecosystem", layout="wide", page_icon="♻️")

# ====== MOCK BLOCKCHAIN LEDGER ======
if "blockchain" not in st.session_state:
    st.session_state.blockchain = []
    st.session_state.user_wallet = {"GreenCoin": 0, "ETH": 0.01}  # mock wallet
    st.session_state.requests = []

def add_block(data):
    prev_hash = st.session_state.blockchain[-1]["hash"] if st.session_state.blockchain else "0" * 64
    block = {
        "index": len(st.session_state.blockchain),
        "timestamp": datetime.now().isoformat(),
        "data": data,
        "prev_hash": prev_hash,
        "hash": hashlib.sha256((str(data) + prev_hash).encode()).hexdigest()
    }
    st.session_state.blockchain.append(block)

# ====== MOCK AI VISION ENGINE ======
def ai_estimate_waste(image_desc: str):
    """
    Simulasi AI Vision: dari deskripsi foto, estimasi jenis & berat
    Dalam versi nyata: pakai model image classifier + object detection
    """
    waste_map = {
        "plastic bottles": ("plastic", 2.3),
        "cardboard box": ("paper", 1.8),
        "old laptop": ("e-waste", 3.1),
        "aluminum cans": ("metal", 1.2),
        "glass jars": ("glass", 2.7),
    }
    for key, val in waste_map.items():
        if key in image_desc.lower():
            return val
    # fallback
    return ("mixed", round(len(image_desc) * 0.1, 1))

# ====== TOKEN CONVERSION RULE ======
TOKEN_RATE = {
    "plastic": 10,   # 1 kg = 10 GreenCoin
    "paper": 8,
    "metal": 15,
    "glass": 6,
    "e-waste": 20,
    "mixed": 5
}

# ====== UI ======
st.title("♻️ SortSmart – Blockchain Waste Ecosystem")
st.caption("Foto sampah → AI estimasi → Pickup → Dapat GreenCoin (on-chain)")

# Sidebar: Wallet & Ledger
with st.sidebar:
    st.header("👛 My Wallet")
    st.metric("GreenCoin", st.session_state.user_wallet["GreenCoin"])
    st.metric("ETH (Gas)", f"{st.session_state.user_wallet['ETH']:.4f}")
    
    st.divider()
    st.subheader("⛓️ Last 3 Blocks")
    for block in st.session_state.blockchain[-3:][::-1]:
        st.caption(f"Block #{block['index']} · {block['data'].get('type', 'tx')}")
    
    if st.button("View Full Ledger", key="ledger_btn"):
        st.session_state.show_ledger = True

# Main Tabs
tab1, tab2, tab3 = st.tabs(["📸 Upload Waste Photo", "🚛 Pickup Requests", "📊 My Rewards"])

# Tab 1: Upload Photo & AI Estimate
with tab1:
    st.subheader("1. Upload Photo of Your Waste")
    st.write("AI will estimate type and weight from your photo description (simulated).")
    
    user_desc = st.text_input(
        "Describe your waste photo (e.g., 'plastic bottles and cardboard')",
        placeholder="e.g., old laptop, plastic bottles, glass jars..."
    )
    
    if st.button("🔍 Analyze with AI") and user_desc:
        waste_type, weight = ai_estimate_waste(user_desc)
        st.success(f"✅ AI Result: **{waste_type.title()}** | **{weight} kg**")
        
        tokens = int(weight * TOKEN_RATE.get(waste_type, 5))
        st.info(f"💡 Estimated Reward: **{tokens} GreenCoin** after successful pickup")
        
        if st.button("✅ Confirm & Record on Blockchain", key="confirm_waste"):
            # Simpan request
            req_id = f"REQ-{int(time.time())}"
            request = {
                "req_id": req_id,
                "waste_type": waste_type,
                "weight_kg": weight,
                "tokens_earned": tokens,
                "status": "Pending",
                "timestamp": datetime.now()
            }
            st.session_state.requests.append(request)
            
            # Catat di blockchain
            add_block({
                "type": "waste_registered",
                "req_id": req_id,
                "waste_type": waste_type,
                "weight_kg": weight,
                "user": "user_001"
            })
            st.balloons()
            st.success("Waste registered on blockchain! 🌍")

# Tab 2: Pickup Management
with tab2:
    st.subheader("2. Pickup Requests")
    if not st.session_state.requests:
        st.info("No waste registered yet. Go to 'Upload Waste Photo' to start.")
    else:
        for i, req in enumerate(st.session_state.requests):
            if req["status"] == "Pending":
                with st.expander(f"📦 {req['req_id']} – {req['waste_type'].title()} ({req['weight_kg']} kg)"):
                    st.write(f"**Reward**: {req['tokens_earned']} GreenCoin")
                    if st.button("📞 Request Pickup", key=f"pickup_{i}"):
                        req["status"] = "Assigned"
                        add_block({
                            "type": "pickup_assigned",
                            "req_id": req["req_id"],
                            "vendor": "vendor_eco1",
                            "fee_eth": 0.001
                        })
                        st.session_state.user_wallet["ETH"] -= 0.001
                        st.success("Vendor assigned! Pickup will arrive soon.")
            
            elif req["status"] == "Assigned":
                st.warning(f"🚛 Pickup in progress for {req['req_id']}")
                if st.button("✅ Mark as Completed", key=f"complete_{i}"):
                    req["status"] = "Completed"
                    st.session_state.user_wallet["GreenCoin"] += req["tokens_earned"]
                    add_block({
                        "type": "pickup_completed",
                        "req_id": req["req_id"],
                        "tokens_awarded": req["tokens_earned"]
                    })
                    st.balloons()
                    st.success(f"🎉 You earned {req['tokens_earned']} GreenCoin!")

# Tab 3: Rewards & Ledger
with tab3:
    st.subheader("3. My GreenCoin Rewards")
    st.write("All rewards are recorded on-chain and non-transferable (eco-token).")
    
    completed = [r for r in st.session_state.requests if r["status"] == "Completed"]
    if completed:
        df = pd.DataFrame(completed)[["req_id", "waste_type", "weight_kg", "tokens_earned"]]
        st.dataframe(df, use_container_width=True)
    else:
        st.info("Complete your first pickup to earn GreenCoin!")
    
    if st.session_state.show_ledger:
        st.divider()
        st.subheader("Full Blockchain Ledger")
        for block in st.session_state.blockchain:
            st.json(block)

# Footer
st.divider()
st.caption("SortSmart v2.0 – Blockchain-Powered Circular Economy | All transactions are immutable and transparent")
