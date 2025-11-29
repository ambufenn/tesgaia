import streamlit as st

# ====== CONFIG ======
st.set_page_config(
    page_title="SortSmart – Edit Project Details",
    page_icon="♻️",
    layout="centered"
)

# ====== UI ======
st.title("Edit Project Details")
st.markdown("Manage your project's documents and datasets here.")

# Project Title
project_title = st.text_input(
    "Project Title",
    value="SortSmart – A Household Waste Sorting & On-Demand Pickup App with Vendor Choice",
    key="project_title"
)

# Application Use Case
use_case = st.text_area(
    "Application Use Case",
    value=("SortSmart is a mobile app connecting households with verified recycling vendors "
           "for on-demand waste pickup. It offers a competitive marketplace with transparent "
           "pricing and vendor selection based on waste type, ratings, and availability, "
           "fostering a user-driven circular economy."),
    height=120,
    key="use_case"
)

# High-Level Design
design = st.text_area(
    "High-Level Design",
    value=("The system comprises a user mobile app for waste input and vendor selection, "
           "a vendor mobile app for managing pickups and pricing, an AI/ML engine for vendor "
           "ranking and fraud detection, and an admin dashboard for vendor management and "
           "monitoring. It integrates with payment gateways, notification services, and "
           "geolocation APIs."),
    height=120,
    key="design"
)

# Sample Dataset Description
st.markdown("### Sample Dataset / Artifacts Description")
st.write(
    "The sample data shows a user request with location coordinates, details of waste items "
    "(type and estimated weight), preferred pickup date, and a link to photo evidence, "
    "demonstrating the data structure used for pickup requests."
)

# Upload Artifacts (UI only – no backend logic)
uploaded_file = st.file_uploader(
    "Upload Artifacts",
    type=["csv", "json", "pdf", "jpg", "png"],
    help="Supported: CSV, JSON, PDF, images"
)

# Display file status
if uploaded_file is not None:
    st.success(f"Selected: {uploaded_file.name}")
else:
    st.info("Tidak ada file yang dipilih")

# Artifact count info
st.caption("You have **0** existing artifact(s). Uploading new files will replace the oldest ones if you exceed the 5-file limit.")

# Action Buttons
col1, col2 = st.columns([1, 2])
with col1:
    if st.button("Cancel"):
        st.info("Changes discarded.")
with col2:
    if st.button("Save Changes"):
        st.success("✅ Project details saved successfully!")
