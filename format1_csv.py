import re
import csv
import PyPDF2
import sys
import pandas as pd

def extract_text_from_pdf(pdf_path):
    text = ""
    with open(pdf_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            text += page.extract_text()
    return text

def write_text_to_csv(text, output_file):
    with open(output_file, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow([text])



# pdf_path = "c:/Users/ADMIN-PC/Desktop/All chrome files/SemVIII_2022-23.pdf"  
# pdf_path ="c:/Users/ADMIN-PC/Desktop/result.pdf"
# pdf_path = "c:/Users/ADMIN-PC/Desktop/All chrome files/1T01538.pdf" 
# pdf_path = "c:/Users/ADMIN-PC/Desktop/All chrome files/format1.pdf"

# output_file = "output.csv"



# pdf_text = extract_text_from_pdf(pdf_path)
# write_text_to_csv(pdf_text, output_file)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python script.py <pdf_path>")
        sys.exit(1)
    
    pdf_path = sys.argv[1]
    output_file = "output.csv"

    pdf_text = extract_text_from_pdf(pdf_path)
    write_text_to_csv(pdf_text, output_file)
