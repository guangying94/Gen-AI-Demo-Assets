from flask import Flask, request, jsonify
import fitz
import io
from datetime import datetime, timezone
import requests
import helper
import json

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return jsonify({"message": "PDF extraction API is running"})

@app.route('/convert-pdf', methods=['POST'])
def convert_pdf_to_image():

    # Initialize sas_url variable as array
    sas_urls = []

    # Create a string using current timestamp, with format YYYY-MM-DD-HH-MM-SS
    current = datetime.now(timezone.utc).strftime("%Y-%m-%d-%H-%M-%S")

    # Get the PDF URL from the request
    pdf_url = request.json['pdf_url']
    
    # Download the PDF from the given URL
    response = requests.get(pdf_url, stream=True)
    pdf_stream = io.BytesIO()
    pdf_stream.write(response.content)
    pdf_stream.seek(0)
    
    # Open the PDF with PyMuPDF
    pdf_document = fitz.open(stream=pdf_stream, filetype='pdf')

    sas_urls = helper.convert_pdf_to_images_and_upload(pdf_document, current)
            
    # Close the PDF document
    pdf_document.close()

    _gptresult = helper.process_with_gpt4(sas_urls)
    gptresult = _gptresult.replace("\\\"", "\"")

    # Convert the string to a JSON object
    gptresult_json = json.loads(gptresult)
    
    return jsonify({"result": gptresult_json, "pdf_img_urls": sas_urls,"processed_datetime": current})

@app.route('/process-private', methods=['POST'])
def process_image_binary():
    current = datetime.now(timezone.utc).strftime("%Y-%m-%d-%H-%M-%S")

    pdf_container = request.json['pdf_container']
    pdf_name = request.json['pdf_name']
    save_images = request.json['save_images']

    # Read pdf from azure storage directly
    imagebase64_list = helper.convert_pdf_to_images_and_generate_binary(pdf_container, pdf_name, save_images, current)

    # process with GPT4
    _gptresult = helper.process_with_gpt4_binary(imagebase64_list)
    gptresult = _gptresult.replace("\\\"", "\"")
    gptresult_json = json.loads(gptresult)

    return jsonify({"result": gptresult_json, "processed_datetime": current})

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0', port=5000)
