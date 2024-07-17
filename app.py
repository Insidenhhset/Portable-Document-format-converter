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
import shutil
from tempfile import TemporaryDirectory
from concurrent.futures import ThreadPoolExecutor
from format3 import convert_pdf_to_excel, csv_to_excel

app = Flask(__name__)

ALLOWED_EXTENSIONS = {'pdf'}
OUTPUT_FOLDER = 'output'
executor = ThreadPoolExecutor(max_workers=4)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def run_subprocess(command):
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if result.returncode != 0:
        raise subprocess.CalledProcessError(result.returncode, command, output=result.stdout, stderr=result.stderr)

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
        os.makedirs(OUTPUT_FOLDER, exist_ok=True)
        with TemporaryDirectory() as temp_dir:
            pdf_path = os.path.join(temp_dir, pdf_file.filename)
            pdf_file.save(pdf_path)
            excel_path = os.path.join(temp_dir, 'output.xlsx')

            try:
                if format_option == 'format1':
                    executor.submit(run_subprocess, ["python", "format1_csv.py", pdf_path]).result()
                    executor.submit(run_subprocess, ["python", "seatno.py", pdf_path]).result()
                    executor.submit(run_subprocess, ["python", "store.py", pdf_path]).result()
                    executor.submit(run_subprocess, ["python", "extra.py", pdf_path]).result()
                    executor.submit(run_subprocess, ["python", "format1.py"]).result()

                    input_file = "output_format1.xlsx"
                    output_file = os.path.join(OUTPUT_FOLDER, "output_format1.xlsx")
                    move_file(input_file, output_file)

                elif format_option == 'format2':
                    executor.submit(run_subprocess, ["python", "format2_csv.py", pdf_path]).result()
                    executor.submit(run_subprocess, ["python", "format2.py"]).result()

                    input_file = "output_format2.xlsx"
                    output_file = os.path.join(OUTPUT_FOLDER, "output_format2.xlsx")
                    move_file(input_file, output_file)

                elif format_option == 'format3':
                    pattern = r"(\b\d{7}\b)((?:.*\n){160})"
                    excluded_ranges = ['2:7', '26:44', '67:74', '93:99', '103:105', '109:112', '137:141', '148:154']
                    convert_pdf_to_excel(pdf_path, pattern, excel_path, excluded_ranges)
                    csv_to_excel("output.csv", excel_path, excluded_ranges)

                    output_file = os.path.join(OUTPUT_FOLDER, 'output_format3.xlsx')
                    shutil.move(excel_path, output_file)
                else:
                    return render_template('index.html', error='Invalid format selected.')

                download_link = f'/download?format={format_option}'
                return render_template('index.html', download_link=download_link)

            except subprocess.CalledProcessError as e:
                error_message = f"Error processing file: Subprocess failed with {str(e)}\nOutput: {e.output}\nError: {e.stderr}"
                return render_template('index.html', error=error_message)
            except Exception as e:
                error_message = f"Error processing file: {str(e)}"
                return render_template('index.html', error=error_message)
    else:
        return render_template('index.html', error='Only PDF files are allowed')

def move_file(input_file, output_file):
    if os.path.exists(input_file):
        if os.path.exists(output_file):
            os.remove(output_file)
        shutil.move(input_file, output_file)
    else:
        raise FileNotFoundError(f"Input file '{input_file}' not found.")

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
