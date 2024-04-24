import re
import csv
import PyPDF2
import pandas as pd
import os

def convert_pdf_to_excel(pdf_path, pattern, excel_path, excluded_ranges):
    # Read PDF file and convert to CSV
    with open(pdf_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        data = []
        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            text = page.extract_text()

            # Find all matches of the pattern in the text
            matches = re.findall(pattern, text)

            # Append matches to data list
            for match in matches:
                data.append([match[0]] + match[1].strip().splitlines())  

    # Write data to CSV file
    with open("output.csv", "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(data)

    # Convert CSV to Excel, excluding specified ranges
    csv_to_excel("output.csv", excel_path, excluded_ranges)
    # print("PDF text has been converted to Excel.")

def csv_to_excel(csv_path, excel_path, excluded_ranges):
    # Parse excluded ranges into a list of tuples
    excluded_ranges = [tuple(map(int, r.split(':'))) for r in excluded_ranges]

    # Read data from CSV file
    data = []
    with open(csv_path, 'r', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            # Exclude values from specified ranges
            filtered_row = []
            for i, value in enumerate(row):
                exclude = any(start <= i <= end for start, end in excluded_ranges)
                if not exclude:
                    filtered_row.append(value)
            data.append(filtered_row)

    # Convert the data to a DataFrame
    df = pd.DataFrame(data)

    # Write DataFrame to Excel file
    df.to_excel(excel_path, index=False, header=False)
    # print("CSV has been converted to Excel.")
    

# Input paths
pdf_path = "./reval_sem2.pdf"
excel_path = 'output_format3.xlsx'

# Define the pattern for extracting data from PDF
pattern = r"(\b\d{7}\b)((?:.*\n){160})"

# Define excluded column ranges
excluded_ranges = ['2:7', '26:44', '67:74', '93:99', '103:105', '109:112', '137:141', '148:154']

# Convert PDF to Excel, excluding specified ranges
convert_pdf_to_excel(pdf_path, pattern, excel_path, excluded_ranges)

