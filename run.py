import sys
from bs4 import BeautifulSoup, NavigableString
import re


def is_empty(element):
    if isinstance(element, NavigableString):
        return not element.string.strip()

    if element.contents:
        for child in element.contents:
            if not is_empty(child):
                return False
    else:
        return True
    if element.string and element.string.strip():
        return False
    return True


def remove_headers(soup):
    # Remove divs containing "Page X"
    for span in soup.find_all("span"):
        if "font-size:39px" in span.get("style", "") or "font-size:22px" in span.get("style", ""):
            span.decompose()
        elif "font-size:15px" in span.get("style", "") and span.get_text().strip() == 'X':
            print("Found X")
            span.decompose()
    for div in soup.find_all("div"):  # page numbers of pdf
        if div.find("a") and "Page " in div.get_text() and len(div.get_text()) < 10:
            div.decompose()
        if div.find("span"):
            span = div.span
            txt = span.get_text().strip()  # page header
            if (
                "ELUCIDÁRIO MADEIRENSE - VOLUME" in txt
                or "ELUCIDÁRIO MADEIRENSE – VOLUME II" in txt
                or "Elucidário Madeirense (O-Z)" in txt
                or "Vol. III" in txt
                or "≡" in txt
            ):
                # print(f"Found {txt}")
                div.decompose()
            elif (
                "font-size:15px" in span.get("style", "")
                or "font-family: Courier; font-size:10px" in span.get("style", "")
            ) and txt.isdigit():  # page numbers
                # print(f"Found {txt}")
                div.decompose()

    # Remove divs containing "ELUCIDÁRIO MADEIRENSE - VOLUME X"
    for div in soup.find_all(
        "div",
        string=lambda text: "ELUCIDÁRIO MADEIRENSE - VOLUME" in text if text else False,
    ):
        div.decompose()

    return soup


def replace_br_with_newline(soup):
    for br in soup.find_all("br"):
        br.replace_with("\n")
    return soup


def compact(soup):
    for div in soup.find_all("div"):
        if "font-family" not in str(div):
            div.decompose()
            continue

        for span in div.find_all("span"):
            style = span.get("style", "")

            if "Bold" in style:
                new_tag = soup.new_tag("b")
                new_tag.string = span.get_text().strip()
                span.replace_with(new_tag)

            elif "Italic" in style:
                new_tag = soup.new_tag("i")
                new_tag.string = span.get_text().strip()
                span.replace_with(new_tag)

            else:
                if span.string:
                    new_tag = soup.new_tag("span")
                    new_tag.string = span.get_text().strip()
                    span.replace_with(new_tag)

        # Replace div with its contents
        div.replace_with_children()

    return soup


def adjust_i_tags(soup):
    # Find all <b> tags
    for b_tag in soup.find_all("b"):
        next_sibling = b_tag.next_sibling
        i_tag = None  # Initialize i_tag

        # Check if the next sibling is a <span> and has '('
        if next_sibling and next_sibling.name == "span" and next_sibling.string and next_sibling.string.strip() == "(":
            i_tag = next_sibling.next_sibling
            if i_tag and i_tag.name == "i":
                # Move '(' into the <i> tag
                i_tag.string = "(" + i_tag.get_text()

                # Remove the <span> containing '('
                next_sibling.decompose()

                # Check if the <i> tag is followed by a <span> with ')'
                if i_tag and i_tag.name == "i":
                    next_sibling = i_tag.next_sibling
                    first_child_of_next_sibling = next_sibling.contents[0].string.lstrip()
                    if (
                        next_sibling
                        and next_sibling.name == "span"
                        and first_child_of_next_sibling.startswith(")")
                    ):
                        # Move ')' into the <i> tag
                        i_tag.string = i_tag.get_text() + ")"
                        contents = next_sibling.contents
                        new_content = re.sub(r'\)\s*\.\s*', '', first_child_of_next_sibling, count=1)
                        # print(f"{b_tag.get_text()} {i_tag.get_text()}: {first_child_of_next_sibling[0:25]}")
                        contents[0].replace_with(NavigableString(new_content))

                        next_sibling.contents = contents
                        new_i = soup.new_tag("i")
                        new_i.string = i_tag.string
                        b_tag.string = b_tag.string + " "
                        b_tag.append(new_i)
                        i_tag.decompose()
    return soup



def remove_newlines_around_tags(
    html_content, tag_name, put_newline_before=False, put_newline_after=False
):
    # Handle opening tag
    if put_newline_before:
        html_content = re.sub(
            f"[\n\s]*<{tag_name}>[\n\s]*", f"\n<{tag_name}>", html_content
        )
    else:
        html_content = re.sub(
            f"[\n\s]*<{tag_name}>[\n\s]*", f" <{tag_name}>", html_content
        )

    # Handle closing tag
    if put_newline_after:
        html_content = re.sub(
            f"[\n\s]*</{tag_name}>[\n\s]*", f"</{tag_name}>\n", html_content
        )
    else:
        html_content = re.sub(
            f"[\n\s]*</{tag_name}>[\n\s]*", f"</{tag_name}>", html_content
        )

    return html_content


def remove_space(html_content):
    # html_content = re.sub(r"<span[^>]*>", "", html_content)
    # html_content = re.sub(r"</span>", "", html_content)
    html_content = re.sub(f"  +", " ", html_content)
    return html_content

def remove_all_styles(soup):
    """
    Remove all style attributes from all tags in a BeautifulSoup object.

    :param soup: BeautifulSoup object to be processed.
    """
    for tag in soup.find_all(style=True):
        del tag['style']
    return soup



def clean_html(input_file, output_file):
    with open(input_file, "r", encoding="utf-8") as file:
        html_content = file.read()

    soup = BeautifulSoup(html_content, "html.parser")

    for tag in soup.find_all(["div", "span"]):
        if is_empty(tag):
            tag.decompose()

    soup = remove_headers(soup)
    # soup = replace_br_with_newline(soup)
    soup = compact(soup)
    soup = adjust_i_tags(soup)
    soup = remove_all_styles(soup)

    # articles = group_articles(soup)
    # print(articles)
    clean_html = soup.prettify()
    clean_html = remove_newlines_around_tags(clean_html, "i", False, False)
    clean_html = remove_newlines_around_tags(clean_html, "span", False, False)
    clean_html = remove_newlines_around_tags(clean_html, "b", True, True)
    clean_html = remove_space(clean_html)

    

    with open(output_file, "w", encoding="utf-8") as file:
        file.write(clean_html)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <input_file.html>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = input_file.rsplit(".", 1)[0] + "_cleaned.html"

    clean_html(input_file, output_file)
    print(f"Cleaned HTML written to {output_file}")
