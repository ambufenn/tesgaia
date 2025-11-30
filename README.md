# Playing Around with Google Cloud: Migrating My Streamlit App to Cloud Run

This repository contains a **Streamlit** application designed to be containerized and deployed to **Google Cloud Run**. The project demonstrates how to package a Python data application with Docker and host it serverlessly on Google Cloud Platform (GCP).

## 📂 Project Structure

```text
tesgaia/
├── data/              # Directory for data files (CSVs, JSONs, etc.)
├── src/               # Source code modules and helper functions
├── app.py             # Main application entry point
├── Dockerfile         # Instructions to build the Docker image
└── requirements.txt   # Python dependencies


Prerequisites
Python 3.8+
Git[1]
1. Clone the Repository

git clone https://github.com/ambufenn/tesgaia.git
cd tesgaia

2. Set Up a Virtual Environment
It is recommended to use a virtual environment to manage dependencies.[1]

# Create virtual environment
python -m venv venv

# Activate it (Windows)
venv\Scripts\activate

# Activate it (macOS/Linux)
source venv/bin/activate


3. Install Dependencies
pip install -r requirements.txt


4. Run the Application

streamlit run app.py

The app should now be running at http://localhost:8501.


☁️ Deployment to Google Cloud Run

Prerequisites
A Google Cloud Platform (GCP) account.
Google Cloud SDK (gcloud CLI) installed and authenticated.
Step 1: Initialize Google Cloud
Login to your Google Cloud account via the terminal:

gcloud auth login


Set your project ID:

gcloud config set project YOUR_PROJECT_ID

Step 2: Enable Necessary Services
Ensure that Cloud Run and Artifact Registry (or Container Registry) APIs are enabled:

gcloud services enable run.googleapis.com
gcloud services enable artifactregistry.googleapis.com
gcloud services enable cloudbuild.googleapis.com


Step 3: Build and Submit the Image
Instead of building locally and pushing, we can use Cloud Build to build the image directly in the cloud and store it in the Google Container Registry (GCR) or Artifact Registry.
Option A: Using Google Container Registry (GCR)

gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/tesgaia-app

Step 4: Deploy to Cloud Run
Deploy the container you just built. Replace the image path with the one you created in Step 3.

gcloud run deploy tesgaia-service \
  --image gcr.io/YOUR_PROJECT_ID/tesgaia-app \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated

Step 5: Access the App


