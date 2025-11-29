# app.py
import streamlit as st
import sys
import os
import time
from datetime import datetime

# Tambahkan src ke path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Impor modul
from src.models.ai_engine import ai_estimate_waste_from_image
from src.config import TOKEN_RATE
from src.core.blockchain import Blockchain, Wallet

# Inisialisasi session state
if "initialized" not in st.session_state:
    st.session_state.blockchain = Blockchain()
    st.session_state.wallet = Wallet()
    st.session_state.user_location = "-6.2088, 106.8456"  # Jakarta
    st.session_state.show_ledger = False
    st.session_state.last_analysis = None
    st.session_state.initialized = True

# ====== CONFIG ======
st.set_page_config(page_title="SortSmart – Blockchain Waste Ecosystem", layout="wide", page_icon="♻️")

# ====== SIDEBAR ======
with st.sidebar:
    st.header("👛 My Wallet")
    st.metric("GreenCoin", st.session_state.wallet.green_coin)
    st.metric("ETH (Gas)", f"{st.session_state.wallet.eth:.4f}")
    
    st.divider()
    st.subheader("⛓️ Last 3 Blocks")
    for block in st.session_state.blockchain.get_last_blocks():
        st.caption(f"Block #{block['index']} · {block['data'].get('type', 'tx')}")
    
    if st.button("View Full Ledger"):
        st.session_state.show_ledger = True

# ====== MAIN ======
st.title("♻️ SortSmart – Blockchain Waste Ecosystem")
st.caption("Upload photo → AI estimates → Choose vendor → Get GreenCoin")

tab1, tab2, tab3 = st.tabs(["📸 Upload Waste", "🚛 Pickup Requests", "📊 My Rewards"])

# Tab 1: Upload
with tab1:
    st.subheader("1. Upload Photo of Your Waste")
    with st.form("upload_form"):
        uploaded_file = st.file_uploader("Choose an image (JPG/PNG)", type=["jpg", "jpeg", "png"])
        submitted = st.form_submit_button("🔍 Analyze with AI")
        
        if submitted and uploaded_file:
            waste_type, weight = ai_estimate_waste_from_image(uploaded_file)
            tokens = int(weight * TOKEN_RATE.get(waste_type, 5))
            st.session_state.last_analysis = {
                "waste_type": waste_type,
                "weight_kg": weight,
                "tokens_earned": tokens,
                "image": uploaded_file
            }
            st.rerun()

    if st.session_state.last_analysis:
        a = st.session_state.last_analysis
        st.image(a["image"], width=300)
        st.success(f"✅ **{a['waste_type'].title()}** | **{a['weight_kg']} kg**")
        st.info(f"💡 Reward: **{a['tokens_earned']} GreenCoin** after pickup")
        
        if st.button("✅ Confirm & Record on Blockchain"):
            req_id = f"REQ-{int(time.time())}"
            request = {
                "req_id": req_id,
                "waste_type": a["waste_type"],
                "weight_kg": a["weight_kg"],
                "tokens_earned": a["tokens_earned"],
                "status": "Pending"
            }
            st.session_state.blockchain.requests.append(request)
            st.session_state.blockchain.add_block({
                "type": "waste_registered",
                "req_id": req_id,
                "waste_type": a["waste_type"],
                "weight_kg": a["weight_kg"]
            })
            st.session_state.last_analysis = None
            st.rerun()

# Tab 2: Pickup (sederhana dulu – fokus ke alur utama)
with tab2:
    st.subheader("2. Pickup Requests")
    if not st.session_state.blockchain.requests:
        st.info("No requests yet. Upload waste first!")
    else:
        for i, req in enumerate(st.session_state.blockchain.requests):
            status_badge = {
                "Pending": "🟡",
                "Assigned": "🔵",
                "Completed": "✅"
            }.get(req["status"], "❓")
            
            with st.expander(f"{status_badge} {req['req_id']} – {req['waste_type'].title()} ({req['weight_kg']} kg)"):
                st.write(f"**Reward**: {req['tokens_earned']} GreenCoin")
                st.write(f"**Location**: {st.session_state.user_location}")
                
                if req["status"] == "Pending":
                    if st.button("📞 Request Pickup", key=f"pickup_{i}"):
                        req["status"] = "Assigned"
                        st.session_state.blockchain.add_block({
                            "type": "pickup_assigned",
                            "req_id": req["req_id"],
                            "vendor": "vendor_eco1"
                        })
                        st.rerun()
                
                elif req["status"] == "Assigned":
                    if st.button("✅ Mark as Completed", key=f"complete_{i}"):
                        req["status"] = "Completed"
                        st.session_state.wallet.green_coin += req["tokens_earned"]
                        st.session_state.blockchain.add_block({
                            "type": "pickup_completed",
                            "req_id": req["req_id"],
                            "tokens_awarded": req["tokens_earned"]
                        })
                        st.balloons()

# Tab 3: Rewards & Ledger
with tab3:
    st.subheader("3. My GreenCoin Rewards")
    st.write("All rewards are recorded on-chain and non-transferable (eco-token).")
    
    # Tampilkan hanya request yang Completed
    completed = [r for r in st.session_state.blockchain.requests if r["status"] == "Completed"]
    if completed:
        # Siapkan DataFrame untuk tampilan rapi
        df_display = []
        for r in completed:
            df_display.append({
                "Request ID": r["req_id"],
                "Waste Type": r["waste_type"].title(),
                "Weight (kg)": r["weight_kg"],
                "GreenCoin Earned": r["tokens_earned"]
            })
        st.dataframe(df_display, use_container_width=True)
    else:
        st.info("Complete your first pickup to earn GreenCoin!")
    
    # Tampilkan Full Ledger jika diaktifkan
    if st.session_state.show_ledger:
        st.divider()
        st.subheader("⛓️ Full Blockchain Ledger")
        st.caption("Immutable record of all transactions")
        # Tampilkan sebagai satu JSON array yang valid
        st.json(st.session_state.blockchain.chain)
st.divider()
st.caption("SortSmart v2.2 – Modular GAIA Lab Project | AI + Blockchain for Waste Economy")
