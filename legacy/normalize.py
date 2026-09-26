import sys
import unicodedata

def remove_accents(input_str):
    nfkd_form = unicodedata.normalize('NFKD', input_str)
    return "".join([c for c in nfkd_form if not unicodedata.combining(c)])

def process_text(text):
    text = remove_accents(text)
    text = text.replace('\n', '')
    text = text.replace('.', '.\n')
    text = text.replace(',', ',\n')
    return text

if __name__ == "__main__":
    for line in sys.stdin:
        processed_line = process_text(line)
        sys.stdout.write(processed_line)
