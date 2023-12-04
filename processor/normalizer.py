import sys
import unicodedata
import re
import difflib
from bs4 import BeautifulSoup


def remove_accents(input_str):
    nfkd_form = unicodedata.normalize("NFKD", input_str)
    return "".join([c for c in nfkd_form if not unicodedata.combining(c)])


def process_text(text):
    text = remove_accents(text)
    text = text.replace("\n", "")
    text = text.replace(".", ".\n")
    text = text.replace(",", ",\n")
    return text


def remove_html_tags(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    return soup.get_text()


def normalize(text):
    text = remove_html_tags(text)
    text = process_text(text)
    return text


def get_similarity_score_exact(str1, str2):
    # Splitting both strings into sentences
    str1 = normalize(str1)
    str2 = normalize(str2)

    sentences_str1 = [s.strip() for s in str1.split(".") if s.strip()]
    sentences_str2 = [s.strip() for s in str2.split(".") if s.strip()]

    # Calculate similarity score for each sentence
    score = 0
    comparisons = min(len(sentences_str1), len(sentences_str2))
    for i in range(comparisons):
        score += difflib.SequenceMatcher(None, sentences_str1[i], sentences_str2[i]).ratio()

    # Adjust score for any additional or missing sentences
    max_length = max(len(sentences_str1), len(sentences_str2))
    if max_length > comparisons:
        score += (max_length - comparisons) * 0.5  # Penalize for additional/missing sentences

    # Normalize the score
    return score / max_length


def find_closest_match(str1, str2_list):
    max_score = 0
    closest_match = None
    for s in str2_list:
        score = difflib.SequenceMatcher(None, str1, s).ratio()
        if score > max_score:
            max_score = score
            closest_match = s
    return closest_match, max_score


def get_similarity_score_exact(str1, str2):
    # Splitting both strings into sentences
    str1 = normalize(str1)
    str2 = normalize(str2)

    # any period, question mark, exclamation mark, new line means a new sentence
    eos_regex = re.compile(r"[.?!\n]+")
    sentences_str1 = [s.strip() for s in eos_regex.split(str1) if s.strip()]
    sentences_str2 = [s.strip() for s in eos_regex.split(str2) if s.strip()]

    # Calculate similarity score for each sentence
    score = 0
    comparisons = min(len(sentences_str1), len(sentences_str2))
    for i in range(comparisons):
        score += difflib.SequenceMatcher(None, sentences_str1[i], sentences_str2[i]).ratio()

    # Adjust score for any additional or missing sentences
    max_length = max(len(sentences_str1), len(sentences_str2))
    if max_length > comparisons:
        score += (max_length - comparisons) * 0.5  # Penalize for additional/missing sentences

    # Normalize the score
    return score / max_length


def get_similarity_score(str1, str2):
    # Splitting both strings into sentences
    THRESHOLD = 0.9
    str1 = normalize(str1)
    str2 = normalize(str2)

    eos_regex = re.compile(r"[.?!\n]+")
    sentences_str1 = [s.strip() for s in eos_regex.split(str1) if s.strip()]
    sentences_str2 = [s.strip() for s in eos_regex.split(str2) if s.strip()]
    # sentences_str1 = [s.strip() for s in str1.split(".") if s.strip()]
    # sentences_str2 = [s.strip() for s in str2.split(".") if s.strip()]

    # Calculate similarity score for each sentence
    score = 0

    for s in sentences_str1:
        closest_match, max_score = find_closest_match(s, sentences_str2)
        # if max_score <= THRESHOLD:
        #     print(
        #         f"A: {s}\nB: {closest_match}\nScore: {round(100*max_score,2)}\n-----------------------------------------"
        #     )
        if max_score > THRESHOLD:
            score += max_score
    return score / len(sentences_str1)
