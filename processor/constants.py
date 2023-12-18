import locale
import re

from bs4 import BeautifulSoup


REIS_PATTERN = r"([0-9]+\.)?[0-9]+:[0-9]+\$[0-9]+"


DEFAULT_MESSAGE_SIZE_THRESHOLD = 8000

DEFAULT_MAX_RETRIES = 4
DEFAULT_INSTRUCTIONS_FILE = "instructions/to_json_ai_revised.txt"


DEFAULT_SIMPLE_GPT_MODEL = "gpt-3.5-turbo-1106"
DEFAULT_COMPLEX_GPT_MODEL = "gpt-4-1106-preview"


def extract_articles_from_html(html_file):
    with open(html_file, "r") as f:
        soup = BeautifulSoup(f, "html.parser")
        divs = soup.find_all("div", class_="article")
        return [str(div) for div in divs]
    
def extract_articles_from_string(html_string):
    soup = BeautifulSoup(html_string, "html.parser")
    divs = soup.find_all("div", class_="article")
    return [str(div) for div in divs]