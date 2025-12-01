import streamlit as st
import requests

# -----------------------------
# Configuration
# -----------------------------
FASTAPI_URL = "http://127.0.0.1:8000"  # backend URL
UPLOAD_ENDPOINT = f"{FASTAPI_URL}/api/upload-file"
GENERATE_ENDPOINT = f"{FASTAPI_URL}/api/generate-report"

st.title("📄 RAG Report Generator")

# -----------------------------
# File Upload Section
# -----------------------------
st.header("1️⃣ Upload File")
uploaded_file = st.file_uploader("Choose a file (PDF, DOCX, CSV)", type=["pdf", "docx", "csv"])

if uploaded_file is not None:
    st.success(f"File selected: {uploaded_file.name}")
    
    files = {"file": (uploaded_file.name, uploaded_file, uploaded_file.type)}
    
    if st.button("Upload to Backend"):
        with st.spinner("Uploading..."):
            try:
                response = requests.post(UPLOAD_ENDPOINT, files=files)
                if response.status_code == 200:
                    st.success("✅ File successfully uploaded to backend!")
                    st.json(response.json())
                else:
                    st.error(f"❌ Upload failed: {response.status_code}")
                    st.write(response.text)
            except Exception as e:
                st.error(f"Error connecting to backend: {e}")

# -----------------------------
# Generate Report Section
# -----------------------------
st.header("2️⃣ Generate Report")
if st.button("Generate Report"):
    with st.spinner("Generating report..."):
        try:
            response = requests.post(GENERATE_ENDPOINT)
            if response.status_code == 200:
                st.success("✅ Report generated successfully!")
                result = response.json()
                st.json(result)

                # If the backend returns a file URL or bytes, you can add a download link
                if "report_url" in result:
                    st.markdown(f"[Download Report]({result['report_url']})")
            else:
                st.error(f"❌ Report generation failed: {response.status_code}")
                st.write(response.text)
        except Exception as e:
            st.error(f"Error connecting to backend: {e}")
