import sys
import re
import csv
import PyPDF2

def convert_pdf_to_csv(pdf_path):
    with open(pdf_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        with open("format2.csv", "w", newline="") as csvfile:
            writer = csv.writer(csvfile)
            for page_num in range(len(reader.pages)):
                page = reader.pages[page_num]
                text = page.extract_text()
                lines = text.split("\n")
                for line in lines:
                    # Remove all spaces from the line
                    line_without_spaces = re.sub(r"\s+", "", line)
                    # Write the line to the CSV file
                    writer.writerow([line_without_spaces])

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python script.py <pdf_path>")
        sys.exit(1)
    
    pdf_path = sys.argv[1]
    convert_pdf_to_csv(pdf_path)
