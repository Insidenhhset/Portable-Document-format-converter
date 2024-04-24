import re
import sys
import csv
import PyPDF2
import pandas as pd

# For Student seat no and names 
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
        # writer.writerow(["Text"])
        writer.writerow([text])



# pdf_path = "c:/Users/ADMIN-PC/Desktop/All chrome files/SemVIII_2022-23.pdf"  
# pdf_path = "c:/Users/ADMIN-PC/Desktop/All chrome files/1T01538.pdf" 
# pdf_path = "c:/Users/ADMIN-PC/Desktop/All chrome files/format1.pdf"

output_file = "seatno.csv"



# pdf_text = extract_text_from_pdf(pdf_path)
# write_text_to_csv(pdf_text, output_file)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python script.py <pdf_path>")
        sys.exit(1)
    
    pdf_path = sys.argv[1]
    output_file = "seatno.csv"
    
    pdf_text = extract_text_from_pdf(pdf_path)
    write_text_to_csv(pdf_text, output_file)



def remove_name_content1(input_file, output_file):
    with open(input_file, 'r', newline='', encoding='utf-8') as infile:
        file_content = infile.read()

    sections = file_content.split('\n')
    modified_sections = []
    for section in sections:
        has_seven_or_eight_digit = re.search(r'\b\d{8}\b|\b\d{7}\b', section)
        if has_seven_or_eight_digit:
            # Define the pattern to match and remove name content along with data after the name in the same line
            pattern = r'\b[A-Z][A-Z\s/]+.*'  # Pattern to match name content and data after it
            # Remove name content and data after the name from the section
            modified_section = re.sub(pattern, '', section)
        else:
            modified_section = section
        modified_sections.append(modified_section)

    modified_content = '\n'.join(modified_sections)
    
    with open(output_file, 'w', newline='', encoding='utf-8') as outfile:
        outfile.write(modified_content)

# Example usage:
remove_name_content1('./seatno.csv', './seatno.csv')
# print("Name content and data after name removed from the CSV file.")