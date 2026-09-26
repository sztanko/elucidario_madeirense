import sys
import re
import logging

def create_regex_pattern(search_string: str) -> str:
    """
    Converts a string into a regex pattern that matches alphanumeric characters in sequence,
    allowing any run of non-alphanumeric characters to be matched by a single wildcard block.
    """
    result = []
    last_was_special = False

    for char in search_string:
        if char.isalnum():
            result.append(char)
            last_was_special = False
        else:
            if not last_was_special:
                result.append('[^a-zA-Z0-9]*')
                last_was_special = True

    return ''.join(result)

def extract_article_content_old(text: str, begins_with: str, ends_with: str, next_start_with: str = None) -> str:
    """
    Extracts the portion of text between the first match of 'begins_with' and the first match of 'ends_with'.
    If 'ends_with' isn't found but 'next_start_with' is provided, that is used as an alternative boundary.
    """
    start_pattern = create_regex_pattern(begins_with)
    end_pattern = create_regex_pattern(ends_with)
    start_match = re.search(start_pattern, text, re.IGNORECASE)

    if not start_match:
        sys.stderr.write(f"Start pattern not found: {begins_with}\n")
        return text

    after_start = text[start_match.end():]
    end_match = re.search(end_pattern, after_start, re.IGNORECASE)

    if not end_match:
        if next_start_with:
            sys.stderr.write(f"Trying next start: {next_start_with}\n")
            next_start_pattern = create_regex_pattern(next_start_with)
            next_start_match = re.search(next_start_pattern, after_start, re.IGNORECASE)
            if next_start_match:
                return after_start[:next_start_match.start()]
            else:
                sys.stderr.write(f"Next start not found: {next_start_with}. Using the entire remaining text.\n")
                return after_start
        sys.stderr.write(f"End pattern not found: {ends_with}. Using the entire remaining text.\n")
        return after_start

    return after_start[:end_match.end()]


def extract_article_content(text: str, begins_with: str, ends_with: str, next_start_with: str = None) -> str:
    """
    Extracts the portion of text between the first match of 'begins_with' and 'ends_with'.
    If 'ends_with' isn't found but 'next_start_with' is provided, that is used as an alternative boundary.
    If the start or end isn't found, the function will retry recursively by trimming the search strings
    (begins_with[1:] or ends_with[:-1]) if they remain at least 20 characters.
    """
    start_pattern = create_regex_pattern(begins_with)
    end_pattern = create_regex_pattern(ends_with)

    # Attempt to find the start
    start_match = re.search(start_pattern, text, re.IGNORECASE)
    if not start_match:
        if len(begins_with) > 20:
            sys.stderr.write(f"Start not found. Retrying with begins_with[1:]: {begins_with[1:]}\n")
            return extract_article_content(text, begins_with[1:], ends_with, next_start_with)
        sys.stderr.write(f"Start pattern not found and too short to trim: {begins_with}\n")
        return text

    # Attempt to find the end
    after_start = text[start_match.start():]
    end_match = re.search(end_pattern, after_start, re.IGNORECASE)
    if end_match:
        return after_start[:end_match.end()]

    # If no end match, try next_start_with if provided
    if next_start_with:
        sys.stderr.write(f"End not found. Trying next start: {next_start_with}\n")
        next_start_pattern = create_regex_pattern(next_start_with)
        next_start_match = re.search(next_start_pattern, after_start, re.IGNORECASE)
        if next_start_match:
            return after_start[:next_start_match.start()]

    # If end still not found, try trimming ends_with if possible
    if len(ends_with) > 20:
        sys.stderr.write(f"End not found. Retrying with ends_with[:-1]: {ends_with[:-1]}\n")
        return extract_article_content(text, begins_with, ends_with[:-1], next_start_with)

    sys.stderr.write(f"End pattern not found and too short to trim: {ends_with}. Using the entire remaining text.\n")
    return after_start


def normalize_newlines(text: str) -> str:
    return re.sub(r"\n{2,}", "\n", text)