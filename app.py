import os
import PyPDF2
import pyttsx3
import streamlit as st
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
import threading

# Flask app setup
app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

def extract_text_from_pdf(pdf_path):
    text = ""
    with open(pdf_path, "rb") as pdf_file:
        reader = PyPDF2.PdfReader(pdf_file)
        for page in reader.pages:
            text += page.extract_text() + "\n"
    return text.strip()

@app.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return jsonify({"error": "No file part"})
    
    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No selected file"})
    
    file_path = os.path.join(app.config["UPLOAD_FOLDER"], secure_filename(file.filename))
    file.save(file_path)
    extracted_text = extract_text_from_pdf(file_path)
    
    return jsonify({"text": extracted_text})

@app.route("/convert_to_speech", methods=["POST"])
def convert_to_speech():
    data = request.get_json()
    text = data.get("text", "")
    
    if not text:
        return jsonify({"error": "No text provided"})
    
    audio_path = "static/output.mp3"
    engine = pyttsx3.init()
    engine.save_to_file(text, audio_path)
    engine.runAndWait()
    
    return jsonify({"audio_url": audio_path})

def run_flask():
    app.run(debug=True, use_reloader=False)

# Start Flask in a separate thread
flask_thread = threading.Thread(target=run_flask, daemon=True)
flask_thread.start()

# Streamlit UI
st.title("PDF to Speech Converter")

uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])
if uploaded_file is not None:
    file_path = os.path.join(UPLOAD_FOLDER, uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    extracted_text = extract_text_from_pdf(file_path)
    st.text_area("Extracted Text", extracted_text, height=250)
    
    if st.button("Convert to Speech"):
        engine = pyttsx3.init()
        audio_path = "output.mp3"
        engine.save_to_file(extracted_text, audio_path)
        engine.runAndWait()
        st.audio(audio_path, format="audio/mp3")