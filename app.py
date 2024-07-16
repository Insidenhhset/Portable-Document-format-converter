"""
Portable Document Format Converter
Author: Nitesh shinde
Date: 23/04/2024

Description:
This script is a Flask application for converting PDF files to Excel format. It provides a web interface for users to upload PDF files and select conversion options.

Credits:
- Developed by Nitesh shinde
- Contact: nitesh.shinde062@gmail.com
"""
from flask import Flask, render_template, request, send_file
import subprocess
import os
import pandas as pd
import re
import sys
import csv
import PyPDF2
import shutil
from tempfile import TemporaryDirectory
from format3 import convert_pdf_to_excel, csv_to_excel

app = Flask(__name__)

ALLOWED_EXTENSIONS = {'pdf'}
OUTPUT_FOLDER = '/tmp/output'

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'pdfFile' not in request.files:
        return render_template('index.html', error='No PDF file part')

    pdf_file = request.files['pdfFile']
    format_option = request.form.get('format')

    if pdf_file and allowed_file(pdf_file.filename):
        # Create the output folder if it doesn't exist
        os.makedirs(OUTPUT_FOLDER, exist_ok=True)

        # Create a temporary directory
        with TemporaryDirectory() as temp_dir:
            pdf_path = os.path.join(temp_dir, pdf_file.filename)
            pdf_file.save(pdf_path)
            excel_path = os.path.join(temp_dir, 'output.xlsx')

            try:
                # Convert PDF to Excel based on selected format
                if format_option == 'format1':
                    subprocess.run(["python", "format1_csv.py", pdf_path])
                    subprocess.run(["python", "seatno.py", pdf_path])
                    subprocess.run(["python", "store.py", pdf_path])
                    subprocess.run(["python", "extra.py", pdf_path])
                    subprocess.run(["python", "format1.py"])

                    input_file = "output_format1.xlsx"
                    output_file = os.path.join(OUTPUT_FOLDER, "output_format1.xlsx")
  
                    if os.path.exists(input_file):
                        if os.path.exists(output_file):
                            os.remove(output_file)
                    shutil.move(input_file, output_file)

                elif format_option == 'format2':
                    subprocess.run(["python", "format2_csv.py", pdf_path])
                    subprocess.run(["python", "format2.py"])

                    input_file = "output_format2.xlsx"
                    output_file = os.path.join(OUTPUT_FOLDER, "output_format2.xlsx")
                    if os.path.exists(output_file):
                        os.remove(output_file)
                    shutil.move(input_file, output_file)

                elif format_option == 'format3':
                    pattern = r"(\b\d{7}\b)((?:.*\n){160})"
                    excluded_ranges = ['2:7', '26:44', '67:74', '93:99', '103:105', '109:112', '137:141', '148:154']
                    convert_pdf_to_excel(pdf_path, pattern, excel_path, excluded_ranges)
                    csv_to_excel(os.path.join('/tmp', "output.csv"), excel_path, excluded_ranges)

                    output_file = os.path.join(OUTPUT_FOLDER, 'output_format3.xlsx')
                    shutil.move(excel_path, output_file)

                else:
                    return render_template('index.html', error='Invalid format selected.')

                download_link = f'/download?format={format_option}'
                return render_template('index.html', download_link=download_link)
            except Exception as e:
                error_message = f"Error processing file: {str(e)}"
                return render_template('index.html', error=error_message)
    else:
        return render_template('index.html', error='Only PDF files are allowed')

@app.route('/download')
def download_excel():
    format_option = request.args.get('format')
    excel_file = os.path.join(OUTPUT_FOLDER, f'output_{format_option}.xlsx')
    return send_file(excel_file, as_attachment=True)

if __name__ == '__main__':
    try:
        app.run(debug=True, port=5000)
    except OSError:
        print("Port 5000 is busy. Trying another port...")
        app.run(debug=True, port=0)  # Let Flask choose an available port
