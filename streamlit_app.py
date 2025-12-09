import streamlit as st
import requests

BACKEND_BASE = "http://127.0.0.1:8000/api"
UPLOAD_ENDPOINT = f"{BACKEND_BASE}/upload"
GENERATE_ENDPOINT = f"{BACKEND_BASE}/generate-report"
DOWNLOAD_ENDPOINT = f"{BACKEND_BASE}/download-report"

st.title("📄 RAG Report Generator (RAG mode)")

uploaded_file = st.file_uploader("Choose a file", type=["csv", "pdf", "docx", "xlsx"])

if uploaded_file is not None:
    if st.button("Upload to backend"):
        with st.spinner("Uploading..."):
            files = {"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
            try:
                r = requests.post(UPLOAD_ENDPOINT, files=files)
                if r.status_code == 200:
                    data = r.json()
                    st.success("Uploaded!")
                    st.json(data)
                    st.session_state["uploaded_file_path"] = data.get("file_path")
                else:
                    st.error("Upload failed")
                    st.json(r.json())
            except Exception as e:
                st.error(f"Error: {e}")

instruction_default = "Create an executive summary and list key risks and recommendations."
instructions = st.text_area("Instructions for the report", value=instruction_default, height=150)
top_k = st.number_input("Top-K retrieved chunks to use", min_value=1, max_value=20, value=5)

if st.button("Generate Report (RAG)"):
    if uploaded_file is None:
        st.error("Please upload a file first.")
    else:
        with st.spinner("Generating report..."):
            payload = {"instructions": instructions, "top_k": int(top_k)}
            files = {"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
            try:
                r = requests.post(GENERATE_ENDPOINT, data=payload, files=files)
                if r.status_code == 200:
                    data = r.json()
                    st.success("Report generated")
                    st.json(data)
                    report_path = data.get("report_path")
                    if report_path:
                        download_url = f"{DOWNLOAD_ENDPOINT}?path={report_path}"
                        st.markdown(f"[Download report]({download_url})")
                else:
                    st.error(f"Failed: {r.status_code}")
                    st.json(r.json())
            except Exception as e:
                st.error(f"Error: {e}")
