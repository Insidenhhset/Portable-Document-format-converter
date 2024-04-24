import csv
import os
import re
import pandas as pd

def extract_seat_numbers_from_csv(file_path):
    csv.field_size_limit(10**9)
    seat_numbers = []
    with open(file_path, 'r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            for item in row:
                matches = re.findall(r'\b\d{7}\b', item)
                seat_numbers.extend(matches)
    return seat_numbers

def extract_names_from_csv(file_path):
    csv.field_size_limit(10**9)
    names = []
    with open(file_path, 'r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            for item in row:
                # matches = re.findall(r'\b\d{7}\s(?:/)?\s*([A-Z][A-Z\s]+?)\s+([A-Z][A-Z\s]+?)(?:\s+([A-Z]+(?:\s+[A-Z]+)*))?\s+', item)
                matches = re.findall(r'(\d{7})\s*(?:/)?\s*([A-Z][A-Z\s]+)' , item)
                for match in matches:
                    full_name = ' '.join(part.strip() for part in match if part.strip())
                    names.append(full_name)
    return names



def parse_line(line):
    # Replace '|' with commas and return as a list
    return line.split('|')

def extract_user_data_from_csv(csv_path):
    # Regular expression pattern to match the line format
    # pattern =  r'(\d{7}/?[A-Z\s]+)\|(\d+)\|(\d+)\|(\d+)\|(\d+)\|(\d+)\|[A-Z0-9]+\|([A-Z]+)'
    pattern  =  r'\b\d{7}'

    # List to store extracted user data
    all_user_data = []

    # Open CSV file and extract text
    with open(csv_path, "r", newline='') as file:
        csv_reader = csv.reader(file)
        
        # Skip the first three lines
        for _ in range(3):
            next(csv_reader)

        user_data = []
        for row in csv_reader:
            text = ' '.join(row)  # Concatenate the row elements into a single string

            # Find all matches in the text
            matches = re.findall(pattern, text)

            # If a match is found, collect next 8 lines as well
            if matches:
                user_data.append(parse_line(text))
                for _ in range(8):
                    row = next(csv_reader, None)
                    if row:
                        text = ' '.join(row)
                        user_data.append(parse_line(text))
                    else:
                        break

                all_user_data.append(user_data)
                user_data = []  # Reset user_data for the next user

    return all_user_data

# Example usage:
csv_path = "./format2.csv"  # Replace with the path to your CSV file
all_user_data = extract_user_data_from_csv(csv_path)
# abc = extract_names_from_csv(csv_path)
# print(abc)




# Input file path
input_file = './format2.csv'

# Function to add '0' at the third position of a 5-digit value
def add_zero_at_third_position(match):
    value = match.group(0)
    if len(value) == 5:
        return value[:2] + '0' + value[2:]
    else:
        return value

# Function to replace all 5-digit values by adding '0' at the third position
def replace_5_digit_values(input_file):
    # Temporary output file
    output_file = 'temp_output_file.csv'
    
    with open(input_file, 'r', newline='', encoding='ISO-8859-1') as infile, \
            open(output_file, 'w', newline='', encoding='ISO-8859-1') as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)
        for row in reader:
            modified_row = [re.sub(r'\b\d{5}\b', add_zero_at_third_position, cell) for cell in row]
            writer.writerow(modified_row)
    
    # Replace the original file with the modified data
    os.remove(input_file)
    os.rename(output_file, input_file)

    print("Modification complete. Input file updated.")

# Call the function to replace all 5-digit values
replace_5_digit_values(input_file)


def remove_spaces(value):
    # Remove any spaces from the value
    return value.replace(' ', '')



def split_values(value):
    if isinstance(value, list):
        value = ' '.join(value)
        
    matches = re.findall(r'\b[A-Z]{2}|[A-Z]{2}|\d{2}[A-Z]|\d{2}@\d{1}|\d{2}|\d[A-Z]|--|\d{2}(?=\d)|\d{1}(?=\d{2})|--|\d{1}@\d{1}|\d{1}(?=[A-Z]{2})|\d+', value)
    
    # Handle special case for consecutive characters like 'RRRRRR'
    if len(matches) == 1 and len(matches[0]) > 2:
        # Split consecutive characters into pairs
        matches = [matches[0][i:i+2] for i in range(0, len(matches[0]), 2)]
    elif len(matches) == 1 and matches[0] == '--':
        matches = ['--']  # Keep only '--' if that's the only match
    
    return ', '.join(matches)


def split_values_pattern_1(value):
    if isinstance(value, list):
        value = ' '.join(value)
    
    # Remove spaces before processing
    # value = remove_spaces(value)
        
    # Use a regular expression to find '----RCC' and split it into '--' and 'RCC'
    matches = re.findall(r'(--+)(RCC)', value)
    
    # If the regex finds any matches, split '----RCC' into '--' and 'RCC'
    if matches:
        # Extract '--' and 'RCC' from each match
        split_matches = [f"{match[0]}, {match[1]}" for match in matches]
        return ', '.join(split_matches)
    else:
        # If no '----RCC' is found, use the original regex to find other patterns
        matches = re.findall(r'\b[A-Z]{2}|\d{3}\.\d{2}|--|\d{2}\.\d{3}|\d{2}\.\d{2}|\d{2}', value)
        return ', '.join(matches)


def split_values_pattern_2(value):
    if isinstance(value, list):
        value = ' '.join(value)
    
    # Remove spaces before processing
    # value = remove_spaces(value)
        
    matches = re.findall(r'\b[A-Z]{2}|--|\d{2}[A-Z]|\d{2}|\d{1}[A-Z]', value)
    
    # Handle special case for consecutive characters like 'RRRRRR'
    if len(matches) == 1 and len(matches[0]) > 2:
        # Split consecutive characters into pairs
        matches = [matches[0][i:i+2] for i in range(0, len(matches[0]), 2)]
    elif len(matches) == 1 and matches[0] == '--':
        matches = ['--']  # Keep only '--' if that's the only match
    
    return ', '.join(matches)

def split_values_pattern_3(value):
    if isinstance(value, list):
        value = ' '.join(value)
    
    # Remove spaces before processing
    # value = remove_spaces(value)
        
    matches = re.findall(r'\b[A-Z]{2}|[A-Z]{2}|--|\d{2}[A-Z]|\d{2}|\d{1}[A-Z]', value)
    
    # Handle special case for consecutive characters like 'RRRRRR'
    if len(matches) == 1 and len(matches[0]) > 2:
        # Split consecutive characters into pairs
        matches = [matches[0][i:i+2] for i in range(0, len(matches[0]), 2)]
    elif len(matches) == 1 and matches[0] == '--':
        matches = ['--']  # Keep only '--' if that's the only match
    
    return ', '.join(matches)


def split_values_pattern_4(value):
    if isinstance(value, list):
        value = ' '.join(value)
        
    # Use regular expression to split the value into groups
    # Two capital letters, two digits followed by one or more letters, two digits,
    # One digit followed by one or more letters, '--', one digit if followed by two letters
    # Or a single digit
    matches = re.findall(r'[A-Z]{2}|[A-Z]|\d{1}\.\d{2}|--|\d{2}\.\d{2}', value)
    
    # Handle special case for consecutive characters like 'RRRRRR'
    if len(matches) == 1 and len(matches[0]) > 2:
        # Split consecutive characters into pairs
        matches = [matches[0][i:i+2] for i in range(0, len(matches[0]), 2)]
    elif len(matches) == 1 and matches[0] == '--':
        matches = ['--']  # Keep only '--' if that's the only match
    
    return ', '.join(matches)



Marks_output = []

for user_data in all_user_data:
    # Concatenate all marks for the user with commas
    # user_marks = (split_values(user_data[1][1:7]) + ',' +
    #               split_values_pattern_1(user_data[1][7]) + ',' +
    #               split_values_pattern_2(user_data[2][6]) + ',' +
    #               split_values_pattern_3(user_data[6][1:5]) + ',' +
    #               split_values_pattern_3(user_data[7][1:5]))
    user_marks = (split_values(user_data[1][1:7]) + ',' +
                  split_values_pattern_1(user_data[1][7]) + ',' +
                  split_values_pattern_2(user_data[2][1:7]) + ',' +
                  split_values_pattern_3(user_data[6][1:7]) + ',' +
                  split_values_pattern_3(user_data[7][1:7]) + ',' +
                   split_values_pattern_4(user_data[3][1:8]) + ',' +
                  split_values_pattern_4(user_data[8][1:5]))
    # Split the concatenated string into a list and append it to Marks_output
    Marks_output.append(user_marks.split(','))



count = 0

# for marks in Marks_output:
#         count += 1
#         print(marks)

        
# Check if all lists in Marks_output have the same size
# if len(set(len(lst) for lst in Marks_output)) == 1:
#     print("All lists in Marks_output have the same size:")
# else:
#     print("Error: Not all lists in Marks_output have the same size!")

# print(count)
# import re

import re

def extract_seat_numbers(all_user_data):
    seat_numbers = []
    for user_data in all_user_data:
        match = re.match(r'^(\d{7})', user_data[0][0])
        if match:
            seat_number = match.group(1)
            seat_numbers.append(seat_number)
        else:
            print("Failed to parse seat number")
    return seat_numbers

seat_numbers = extract_seat_numbers(all_user_data)
# print(seat_numbers)
# print(len(seat_numbers))


import re

def extract_names(all_user_data):
    seat_names = []
    for user_data in all_user_data:
        match = re.match(r'(\d{7})/?([A-Z\s]+)', user_data[0][0])
        if match:
            seat_name = match.group(2)  # Group 2 contains the name
            seat_names.append(seat_name)
        else:
            print("Failed to parse seat number")
    return seat_names

names = extract_names(all_user_data)
# print(names)
# print(len(names))


import pandas as pd
final_data = []
for marks_list in Marks_output:
    # Create a dictionary to store marks data for each user
    row_data = {}
    
    # Iterate over each mark in marks_list
    for i, mark in enumerate(marks_list):
        # Add the mark to the row_data dictionary with a key like 'Mark_1', 'Mark_2', etc.
        row_data[f'Mark_{i+1}'] = mark
    
    # Append the row_data dictionary to the final_data list
    final_data.append(row_data)



# Create a DataFrame for seat_numbers and names
df_info = pd.DataFrame({"Seat Number": seat_numbers, "Name": names})

# Create a DataFrame from the final data (df_marks)
df_marks = pd.DataFrame(final_data)

# Merge the two DataFrames based on their indices
df_merged = pd.concat([df_info, df_marks], axis=1)

# Save the merged DataFrame to an Excel file
output_file = 'output_format2.xlsx'
df_merged.to_excel(output_file, index=False)

print("Marks data has been saved to " + output_file)


