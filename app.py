# app.py
import streamlit as st
import sys
import os
from datetime import datetime
import time

# Tambahkan src ke path agar bisa import
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.models.ai_engine import ai_estimate_waste_from_image
from src.core.blockchain import Blockchain, Wallet
from src.config import TOKEN_RATE

# Initialize session state
if "initialized" not in st.session_state:
    st.session_state.blockchain = Blockchain()
    st.session_state.wallet = Wallet()
    st.session_state.show_ledger = False
    st.session_state.initialized = True

# ====== CONFIG ======
st.set_page_config(page_title="SortSmart – Blockchain Waste Ecosystem", layout="wide", page_icon="♻️")

# ====== UI ======
st.title("♻️ SortSmart – Blockchain Waste Ecosystem")
st.caption("Foto sampah → AI estimasi → Pickup → Dapat GreenCoin (on-chain)")

# Sidebar: Wallet & Ledger
with st.sidebar:
    st.header("👛 My Wallet")
    wallet = st.session_state.wallet
    st.metric("GreenCoin", wallet.green_coin)
    st.metric("ETH (Gas)", f"{wallet.eth:.4f}")
    
    st.divider()
    st.subheader("⛓️ Last 3 Blocks")
    for block in st.session_state.blockchain.get_last_blocks():
        st.caption(f"Block #{block['index']} · {block['data'].get('type', 'tx')}")
    
    if st.button("View Full Ledger", key="ledger_btn"):
        st.session_state.show_ledger = True

# Main Tabs
tab1, tab2, tab3 = st.tabs(["📸 Upload Waste Photo", "🚛 Pickup Requests", "📊 My Rewards"])

# Tab 1: Upload Photo
with tab1:
    st.subheader("1. Upload Photo of Your Waste")
    st.write("Take or upload a photo of your sorted waste. AI will estimate type and weight.")
    
    uploaded_file = st.file_uploader(
        "Choose an image (JPG/PNG)",
        type=["jpg", "jpeg", "png"],
        accept_multiple_files=False
    )
    
    if uploaded_file is not None:
        st.image(uploaded_file, caption="Your waste photo", width=300)
        
        if st.button("🔍 Analyze with AI"):
            waste_type, weight = ai_estimate_waste_from_image(uploaded_file)
            tokens = int(weight * TOKEN_RATE[waste_type])
            
            st.success(f"✅ AI Result: **{waste_type.title()}** | **{weight} kg**")
            st.info(f"💡 Estimated Reward: **{tokens} GreenCoin** after pickup")
            
            if st.button("✅ Confirm & Record on Blockchain", key="confirm_waste"):
                req_id = f"REQ-{int(time.time())}"
                request = {
                    "req_id": req_id,
                    "waste_type": waste_type,
                    "weight_kg": weight,
                    "tokens_earned": tokens,
                    "status": "Pending",
                    "timestamp": datetime.now()
                }
                st.session_state.blockchain.requests.append(request)
                st.session_state.blockchain.add_block({
                    "type": "waste_registered",
                    "req_id": req_id,
                    "waste_type": waste_type,
                    "weight_kg": weight,
                    "user": "user_001"
                })
                st.balloons()
                st.success("Waste registered on blockchain! 🌍")

# Tab 2: Pickup Requests
with tab2:
    st.subheader("2. Pickup Requests")
    requests = st.session_state.blockchain.requests
    if not requests:
        st.info("No waste registered yet. Go to 'Upload Waste Photo' to start.")
    else:
        for i, req in enumerate(requests):
            if req["status"] == "Pending":
                with st.expander(f"📦 {req['req_id']} – {req['waste_type'].title()} ({req['weight_kg']} kg)"):
                    st.write(f"**Reward**: {req['tokens_earned']} GreenCoin")
                    if st.button("📞 Request Pickup", key=f"pickup_{i}"):
                        req["status"] = "Assigned"
                        st.session_state.blockchain.add_block({
                            "type": "pickup_assigned",
                            "req_id": req["req_id"],
                            "vendor": "vendor_eco1",
                            "fee_eth": 0.001
                        })
                        st.session_state.wallet.eth -= 0.001
                        st.success("Vendor assigned! Pickup will arrive soon.")
            
            elif req["status"] == "Assigned":
                st.warning(f"🚛 Pickup in progress for {req['req_id']}")
                if st.button("✅ Mark as Completed", key=f"complete_{i}"):
                    req["status"] = "Completed"
                    st.session_state.wallet.green_coin += req["tokens_earned"]
                    st.session_state.blockchain.add_block({
                        "type": "pickup_completed",
                        "req_id": req["req_id"],
                        "tokens_awarded": req["tokens_earned"]
                    })
                    st.balloons()
                    st.success(f"🎉 You earned {req['tokens_earned']} GreenCoin!")

# Tab 3: Rewards
with tab3:
    st.subheader("3. My GreenCoin Rewards")
    completed = [r for r in st.session_state.blockchain.requests if r["status"] == "Completed"]
    if completed:
        st.dataframe(completed, use_container_width=True)
    else:
        st.info("Complete your first pickup to earn GreenCoin!")
    
    if st.session_state.show_ledger:
        st.divider()
        st.subheader("Full Blockchain Ledger")
        for block in st.session_state.blockchain.chain:
            st.json(block)

st.divider()
st.caption("SortSmart v2.0 – Blockchain-Powered Circular Economy | All transactions are immutable")
