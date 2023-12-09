import locale
import re

from bs4 import BeautifulSoup


REIS_PATTERN = r"([0-9]+\.)?[0-9]+:[0-9]+\$[0-9]+"


DEFAULT_MESSAGE_SIZE_THRESHOLD = 8000

DEFAULT_MAX_RETRIES = 4
DEFAULT_INSTRUCTIONS_FILE = "instructions/to_json_ai_revised.txt"


DEFAULT_SIMPLE_GPT_MODEL = "gpt-3.5-turbo-1106"
DEFAULT_COMPLEX_GPT_MODEL = "gpt-4-1106-preview"


def exrtract_articles_from_html(html_file):
    with open(html_file, "r") as f:
        soup = BeautifulSoup(f, "html.parser")
        divs = soup.find_all("div", class_="article")
        return [str(div) for div in divs]


def convert_portuguese_currency(number_str):
    locale.setlocale(locale.LC_ALL, "pt_BR.UTF-8")
    """
    Converts a Portuguese currency string in the format 'X.Y:Z$W' to a numerical value.
    The conversion assumes 1 conto = 1,000,000 réis.

    Args:
    number_str (str): A string representing the currency in the format 'X.Y:Z$W'.

    Returns:
    int: The numerical value in réis.
    """

    # Splitting the string into contos, hundreds of réis, and réis
    number = int(number_str.replace(".", "").replace("$", "").replace(":", ""))
    formatted_number = locale.format_string("%d", number, grouping=True)

    return formatted_number


def replace_reis(text):
    return re.sub(REIS_PATTERN, lambda g: convert_portuguese_currency(g.group()), text)


def test_conversion():
    locale.setlocale(locale.LC_ALL, "pt_BR.UTF-8")
    number = 123456
    formatted_number = locale.format_string("%d", number, grouping=True)
    print(formatted_number)


if __name__ == "__main__":
    test_conversion()
    text = "Well, this is 1.273:156$226"
    print(replace_reis(text))
