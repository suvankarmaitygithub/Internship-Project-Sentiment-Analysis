import os
import re
import pandas as pd
import csv
import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import cmudict, stopwords
from string import punctuation

# Download NLTK resources
nltk.download('punkt')
nltk.download('cmudict')
nltk.download('stopwords')


# Define the folder path
folder_path = "/Users/suvankarmaity/Downloads/Meghla Internship Project/StopWords"

# Initialize an empty list to store all words
stop_words = []

# Iterate over each file in the folder
for file_name in os.listdir(folder_path):
    if file_name.endswith('.txt'):
        file_path = os.path.join(folder_path, file_name)
        # Open the file and read its contents with the correct encoding
        with open(file_path, 'r', encoding='latin-1') as file:
            # Read the entire content of the file
            file_content = file.read()
            # Split the content into words
            words = file_content.split()
            # Add the words to the list of all words
            stop_words.extend(words)

print("Total number of words:", len(stop_words))

# Saving the file
file_path = "/Users/suvankarmaity/Downloads/Meghla Internship Project/stop_words.txt"

# Open the file in write mode
with open(file_path, "w") as file:
    # Write each word to the file on separate lines
    for word in stop_words:
        file.write(word + "\n")

# Creating a dictionary of Positive and Negative words. We add only those words in the dictionary if they are not found in the Stop Words Lists. 
        
# Read stop words list from the file
def read_stopwords(stopwords_file):
    with open(stopwords_file, 'r', encoding='utf-8') as file:
        stopwords = [line.strip() for line in file]
    return stopwords

# Define the file paths
positive_file = "/Users/suvankarmaity/Downloads/Meghla Internship Project/MasterDictionary/positive-words.txt"
negative_file = "/Users/suvankarmaity/Downloads/Meghla Internship Project/MasterDictionary/negative-words.txt"
stopwords_file = "/Users/suvankarmaity/Downloads/Meghla Internship Project/stop_words.txt"

# Read stop words
stopwords = read_stopwords(stopwords_file)

# Initialize dictionary for positive and negative words
word_dict = {'positive': [], 'negative': []}

# Function to process words from a file
def process_words(file_path, word_list):
    with open(file_path, 'r', encoding='latin-1') as file:
        for line in file:
            word = line.strip()
            # Check if the word is not in the stop words list
            if word not in stopwords:
                word_list.append(word)


# Process positive words
process_words(positive_file, word_dict['positive'])

# Process negative words
process_words(negative_file, word_dict['negative'])

print("Dictionary of positive and negative words without stop words:")
print(word_dict)

# Write positive words to positive_dict.txt
with open("positive_dict.txt", "w") as positive_file:
    for word in word_dict['positive']:
        positive_file.write(word + "\n")

# Write negative words to negative_dict.txt
with open("negative_dict.txt", "w") as negative_file:
    for word in word_dict['negative']:
        negative_file.write(word + "\n")
