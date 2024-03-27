import os
import re
import csv
import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import cmudict, stopwords
from string import punctuation

# Download NLTK resources
nltk.download('punkt')
nltk.download('cmudict')
nltk.download('stopwords')

# Function to count words in a file
def count_words(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        content = file.read()
        word_count = len(content.split())
    return word_count

# Function to load words from file
def load_words_from_file(file_path):
    with open(file_path, 'r') as f:
        return set(word.strip().lower() for word in f)

# Function to count words in a file based on a given set of words
def count_words_in_file(file_path, words):
    with open(file_path, 'r') as f:
        content = f.read().lower()
        return sum(1 if word in words else 0 for word in content.split())

# Function to calculate polarity score and subjectivity score
def calculate_polarity_and_subjectivity_scores(folder_path, positive_file, negative_file):
    positive_words = load_words_from_file(positive_file)
    negative_words = load_words_from_file(negative_file)

    scores = []

    for file_name in os.listdir(folder_path):
        if file_name.endswith('.txt'):
            file_path = os.path.join(folder_path, file_name)
            positive_score = count_words_in_file(file_path, positive_words)
            negative_score = count_words_in_file(file_path, negative_words)
            total_words = count_words(file_path)
            polarity_score = (positive_score - negative_score) / ((positive_score + negative_score) + 0.000001)
            subjectivity_score = (positive_score + negative_score) / (total_words + 0.000001)
            scores.append({
                "File Name": file_name,
                "Positive Score": positive_score,
                "Negative Score": negative_score,
                "Polarity Score": polarity_score,
                "Subjectivity Score": subjectivity_score
            })

    return scores

# Function to count the number of complex words in a list of words
def count_complex_words(words):
    cmu_dict = cmudict.dict()
    complex_word_count = 0
    for word in words:
        syllables = syllable_count(word, cmu_dict)
        if syllables > 2:
            complex_word_count += 1
    return complex_word_count

# Function to count the number of syllables in a word using the CMU Pronouncing Dictionary
def syllable_count(word, cmu_dict):
    if word.lower() in cmu_dict:
        return max([len(list(y for y in x if y[-1].isdigit())) for x in cmu_dict[word.lower()]])
    else:
        return 0

# Function to calculate the average sentence length
def calculate_average_sentence_length(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        content = file.read()
        sentences = sent_tokenize(content)
        words = word_tokenize(content)
        return len(words) / len(sentences) if len(sentences) > 0 else 0

# Function to calculate the percentage of complex words
def calculate_percentage_complex_words(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        content = file.read()
        words = word_tokenize(content)
        total_words = len(words)
        complex_word_count = count_complex_words(words)
        if total_words == 0:
            return 0  # Prevent division by zero
        else:
            return (complex_word_count / total_words) * 100

# Function to calculate the Fog Index for a file
def calculate_fog_index(file_path):
    average_sentence_length = calculate_average_sentence_length(file_path)
    percentage_complex_words = calculate_percentage_complex_words(file_path)
    fog_index = 0.4 * (average_sentence_length + percentage_complex_words)
    return fog_index

# Function to analyze readability metrics for each file
def analyze_readability(folder_path):
    readability_metrics = []

    for file_name in os.listdir(folder_path):
        if file_name.endswith('.txt'):
            file_path = os.path.join(folder_path, file_name)
            average_sentence_length = calculate_average_sentence_length(file_path)
            percentage_complex_words = calculate_percentage_complex_words(file_path)
            fog_index = calculate_fog_index(file_path)
            readability_metrics.append({
                "File Name": file_name,
                "Average Sentence Length": average_sentence_length,
                "Percentage of Complex Words": percentage_complex_words,
                "Fog Index": fog_index
            })

    return readability_metrics

# Function to merge scores and readability metrics and store in CSV
def merge_and_store_data(folder_path, positive_file, negative_file, output_file):
    polarity_subjectivity_scores = calculate_polarity_and_subjectivity_scores(folder_path, positive_file, negative_file)
    readability_metrics = analyze_readability(folder_path)

    merged_data = []

    for score_data, readability_data in zip(polarity_subjectivity_scores, readability_metrics):
        merged_data.append({**score_data, **readability_data})

    # Write data to CSV
    with open(output_file, 'w', newline='') as csvfile:
        fieldnames = merged_data[0].keys()
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for data in merged_data:
            writer.writerow(data)

# Define paths
folder_path = "/Users/suvankarmaity/Downloads/Meghla Internship Project/removed_stopwords_data"
positive_file = "/Users/suvankarmaity/Downloads/Meghla Internship Project/positive_dict.txt"
negative_file = "/Users/suvankarmaity/Downloads/Meghla Internship Project/negative_dict.txt"
output_file = "/Users/suvankarmaity/Downloads/Meghla Internship Project/metrics1_data.csv"

# Merge data and store in CSV
merge_and_store_data(folder_path, positive_file, negative_file, output_file)


# Function to count the number of words and sentences in a file
def count_words_and_sentences(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        content = file.read()
        sentences = sent_tokenize(content)
        words = word_tokenize(content)
        return len(words), len(sentences)

# Function to count the number of complex words in a list of words
def count_complex_words(words):
    cmu_dict = cmudict.dict()
    complex_word_count = 0
    for word in words:
        syllables = syllable_count(word, cmu_dict)
        if syllables > 2:
            complex_word_count += 1
    return complex_word_count

# Function to count the number of syllables in a word using the CMU Pronouncing Dictionary
def syllable_count(word, cmu_dict):
    if word.lower() in cmu_dict:
        return max([len(list(y for y in x if y[-1].isdigit())) for x in cmu_dict[word.lower()]])
    else:
        return 0

# Function to count the total cleaned words in a file
def count_cleaned_words(file_path):
    stop_words = set(stopwords.words('english'))
    cleaned_word_count = 0

    with open(file_path, "r", encoding="utf-8") as file:
        content = file.read()
        words = word_tokenize(content)
        
        # Remove punctuations and stop words
        cleaned_words = [word.lower() for word in words if word.lower() not in stop_words and word.lower() not in punctuation]
        
        cleaned_word_count = len(cleaned_words)

    return cleaned_word_count

# Function to count personal pronouns in text
def count_personal_pronouns(text):
    personal_pronouns = ["I", "we", "my", "ours", "us"]
    # Regular expression pattern to match personal pronouns
    pattern = r'\b(?:' + '|'.join(personal_pronouns) + r')\b'
    # Find all matches of personal pronouns in the text
    matches = re.findall(pattern, text, flags=re.IGNORECASE)
    return len(matches)

# Function to calculate average word length in text
def calculate_average_word_length(text):
    words = word_tokenize(text)
    total_characters = sum(len(word) for word in words)
    total_words = len(words)
    if total_words == 0:
        return 0  # Prevent division by zero
    else:
        return total_characters / total_words

# Function to collect key metrics for each file
def collect_key_metrics_for_files(folder_path):
    data = []

    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)
        if os.path.isfile(file_path):
            with open(file_path, "r", encoding="utf-8") as file:
                content = file.read()
                words, sentences = count_words_and_sentences(file_path)
                cmplx_words = count_complex_words(word_tokenize(content))
                cleaned_words = count_cleaned_words(file_path)
                pronouns = count_personal_pronouns(content)
                avg_word_length = calculate_average_word_length(content)
                data.append([file_name, words / sentences, cmplx_words, cleaned_words, pronouns, avg_word_length])

    return data

# Define the path to the folder containing the files
folder_path = "/Users/suvankarmaity/Downloads/Meghla Internship Project/removed_stopwords_data"

# Collect key metrics for each file in the folder
metrics_data = collect_key_metrics_for_files(folder_path)

# Write the key metrics data into a CSV file
csv_file_path = "/Users/suvankarmaity/Downloads/Meghla Internship Project/metrics2_data.csv"
with open(csv_file_path, "w", encoding="utf-8") as csv_file:
    # Write header
    csv_file.write("File Name,Average Number of Words Per Sentence,Complex Word Count,Cleaned Word Count,Personal Pronoun Count,Average Word Length\n")
    # Write data
    for row in metrics_data:
        csv_file.write(",".join(map(str, row)) + "\n")

print("Key metrics data has been saved to:", csv_file_path)


import pandas as pd

# Read the two CSV files
file1 = pd.read_csv("/Users/suvankarmaity/Downloads/Meghla Internship Project/metrics1_data.csv")
file2 = pd.read_csv("/Users/suvankarmaity/Downloads/Meghla Internship Project/metrics2_data.csv")

# Merge the two files based on the 'File Name' column
merged_data = pd.merge(file1, file2, on='File Name', how='inner')

# Save the merged data to a new CSV file
merged_data.to_csv("Output Data Structure.csv", index=False)

print("Merged data has been saved to: Output Data Structure.csv")