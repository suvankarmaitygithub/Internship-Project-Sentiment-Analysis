import numpy as np
import pandas as pd
import warnings
import requests
from bs4 import BeautifulSoup as bs
import os
import re

warnings.filterwarnings("ignore")

def remove_html_tags(text):
    # Define the regular expression pattern to match HTML tags
    html_tags_pattern = re.compile(r'<[^>]+>')
    # Use sub() method to remove HTML tags
    return html_tags_pattern.sub('', text)

def process_text_file(file_path):
    # Read the content of the text file
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()
    
    # Remove HTML tags from the text
    text = remove_html_tags(text)
    
    # Convert text to lowercase
    text = text.lower()
    
    # Write the modified text back to the file
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(text)

# Reading the input file
df = pd.read_excel('/Users/suvankarmaity/Downloads/Meghla Internship Project/Input.xlsx')

# Starting webscraping
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win 64 ; x64) Apple WeKit /537.36(KHTML , like Gecko) Chrome/80.0.3987.162 Safari/537.36'}

# Define the desired folder path
folder_path = "/Users/suvankarmaity/Downloads/Meghla Internship Project/extracted_data"

for index, row in df.iterrows():
    url = row['URL']
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        soup = bs(response.content, "html.parser")
        H1 = soup.find_all('h1')[0].text
        # Convert heading into a string
        H1 = str(H1)

        # Content
        content_elements = soup.find_all('div', class_='td-post-content tagdiv-type')
        if content_elements:
            content = content_elements[0]
            # Convert content into a string
            content = str(content)
        else:
            print(f"No content found for URL_ID {row['URL_ID']}")
            continue

        # Saving the content into a text file
        try:
            # Concatenate the strings
            combined_text = H1 + "  " + content

            # Select a specific value from the Series as the file name
            file_name = row['URL_ID'] + ".txt"

            # Join folder path with file name
            file_path = os.path.join(folder_path, file_name)

            # Save the combined content to the text file
            with open(file_path, "w") as file:
                file.write(combined_text)

            print(f"Combined text saved to '{file_path}' for URL_ID {row['URL_ID']}.")
        except Exception as e:
            print(f"Error saving content for URL_ID {row['URL_ID']}: {e}")
    else:
        print(f"Error accessing URL {url}. Status code: {response.status_code}")

# Iterate over each file in the folder
for file_name in os.listdir(folder_path):
    if file_name.endswith('.txt'):
        file_path = os.path.join(folder_path, file_name)
        # Process the text file
        print("Processing file:", file_path)
        process_text_file(file_path)
