import locale
import re


def convert_portuguese_currency(number_str):
    """
    Converts a Portuguese currency string in the format 'X.Y:Z$W' to a numerical value.
    The conversion assumes 1 conto = 1,000,000 réis.

    Args:
    number_str (str): A string representing the currency in the format 'X.Y:Z$W'.

    Returns:
    int: The numerical value in réis.
    """
    locale.setlocale(locale.LC_ALL, "pt_BR.UTF-8")
    # Splitting the string into contos, hundreds of réis, and réis
    number = int(number_str.replace(".", "").replace("$", "").replace(":", ""))
    formatted_number = locale.format_string("%d", number, grouping=True)

    return formatted_number


def replace_reis(text):
    return re.sub(REIS_PATTERN, lambda g: convert_portuguese_currency(g.group()), text)
