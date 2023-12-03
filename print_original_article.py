import os
import json
import re

import sys
import unicodedata

from bs4 import BeautifulSoup
from processor.constants import exrtract_articles_from_html



def remove_html_tags(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    return soup.get_text()


def remove_accents(input_str):
    nfkd_form = unicodedata.normalize('NFKD', input_str)
    return "".join([c for c in nfkd_form if not unicodedata.combining(c)])

def process_text(text):
    text = remove_html_tags(text)
    text = remove_accents(text)
    text = text.replace('\n', '')
    text = text.replace('.', '.\n')
    text = text.replace(',', ',\n')
    return text


def print_article(data):
    print(process_text(data))


def main(html_file, filter_by):
    # with open("out.json", "r") as f:
    #    out = json.load(f)
    #    x = unify_chunks(out)
    #    print(json.dumps(x, indent=4, ensure_ascii=False))
    #    return
    articles = exrtract_articles_from_html(html_file)
    
    article_subset = list(filter(lambda a: f">{filter_by}" in a, articles))
    # print(f"Total articles: {len(article_subset)}, {len(merged)} chars")
    for a in article_subset:
        print_article(a)
        


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 3:
        print("Usage: python to_json.py <html_file> article_name")
        sys.exit(1)
    if not os.path.exists(sys.argv[1]):
        print(f"Error: file '{sys.argv[1]}' not found")
        sys.exit(1)    
    main(sys.argv[1], sys.argv[2])
