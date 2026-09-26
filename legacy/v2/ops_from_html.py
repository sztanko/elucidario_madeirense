import re
import json
import sys
from datetime import datetime
import yaml
from bs4 import BeautifulSoup
from llms.utils import extract_article_content

ARTICLE_SIZE_THRESHOLD = 1000

def load_articles(html_string):
    """
    Takes in a string containing the HTML for multiple articles
    and returns an array of transformed article strings.
    """
    sys.stderr.write("Starting to parse articles...\n")

    soup = BeautifulSoup(html_string, "html.parser")
    # Find all the divs that have class='article'
    div_articles = soup.find_all("div", class_="article")

    transformed_articles = []
    
    for idx, div_article in enumerate(div_articles):
        # sys.stderr.write(f"Processing article #{idx+1}\n")

        # Get the h1 (for title)
        h1_tag = div_article.find("h1")
        title_text = h1_tag.get_text(strip=True) if h1_tag else "No Title"

        # Get the content from the 'article_body' div
        body_div = div_article.find("div", class_="article_body")
        if not body_div:
            # If there's no .article_body, skip
            continue

        # Replace <br/> with newlines
        for br in body_div.find_all("br"):
            br.replace_with("\n")

        # Remove all <span> tags but keep their text
        # E.g., <span>some text</span> -> "some text"
        for span in body_div.find_all("span"):
            span.unwrap()

        # Now get the full text content (stripping extra whitespace)
        body_text = body_div.get_text()
        # Optionally, you can clean up extra blank lines or trailing spaces, e.g.:
        lines = [line.strip() for line in body_text.splitlines()]
        # Remove empty lines if you want them gone:
        lines = [line for line in lines if line]  # If you want to remove blank lines
        body_text = "\n".join(lines)

        # Build the final transformed article
        transformed_article = {
            "title": title_text,
            "body": body_text,
        }
        transformed_articles.append(transformed_article)

    sys.stderr.write(f"Finished parsing {len(transformed_articles)} articles.\n")
    return transformed_articles


def dump_yaml(data):

    # Custom presenter for all strings to use the literal style "|"
    def literal_presenter(dumper, data):
        if "\n" in data:
            return dumper.represent_scalar("tag:yaml.org,2002:str", data, style="|")
        return dumper.represent_scalar("tag:yaml.org,2002:str", data)

    # Create a custom Dumper class
    class LiteralDumper(yaml.Dumper):
        pass

    # Register the presenter with the custom Dumper
    LiteralDumper.add_representer(str, literal_presenter)

    # Ensure Unicode characters are not escaped
    LiteralDumper.ignore_aliases = lambda *args: True

    # Dump YAML with the custom Dumper
    return yaml.dump(data, Dumper=LiteralDumper, default_flow_style=False, allow_unicode=True, sort_keys=False)

def extract_article_content_old(text, structure):
    text_with_no_new_lines = text.replace("\n", " ")
    start = structure["begins_with"].replace("\n", " ")
    end = structure["ends_with"].replace("\n", " ")
    start_pos = text_with_no_new_lines.find(start)
    remaining_text = text[start_pos:]
    remaining_text_no_new_lines = remaining_text.replace("\n", " ")
    end_pos = remaining_text_no_new_lines.find(end)
    if end_pos == -1:
        sys.stderr.write(f"End not found: {end} (with start: {start})\n")
        sys.stderr.write(f"Using the whole text as content\n")
        end_pos = len(remaining_text)
    else:
        end_pos += len(end)
    content = remaining_text[0:end_pos]
    return str(content)

def get_article_count(name, text):
    from prompts import detect_articles
    from llms import gemini

    prompt = f"""
    <one_or_more_articles>
    <name>{name}</name>
    <body>
    {text}
    </body>
    </one_or_more_articles>
    """
    out = gemini.run_llm(detect_articles, text)
    out_content = []
    try:
        # sys.stderr.write(f"Response: {out.text}\n")
        content = json.loads(out.text)
        if "articles" not in content:
            sys.stderr.write(f"No articles detected\n")
            sys.stderr.write(json.dumps(content, indent=2))
            raise Exception("No articles detected")        
        num_articles = len(content["articles"])
        if num_articles > 1:
            sys.stderr.write(f"Number of articles: {num_articles}\n")
        sys.stderr.write(f"{content["reason"]}\n")
        if num_articles > 1:
            sys.stderr.write(f"Multiple articles detected\n")
            for i in range(len(content["articles"])):
                c = content["articles"][i]
                sys.stderr.write(f"Article  {i} title: {c["name"]}\n")
                next_prefix = content["articles"][i + 1]["begins_with"] if i + 1 < len(content["articles"]) else content["articles"][i]["ends_with"]
                c["content"] = extract_article_content(text, content["articles"][i]["begins_with"], content["articles"][i]["ends_with"], next_prefix)
                c["length"] = len(c["content"])  # add length of content
                out_content.append(c)
            content["articles"] = out_content
        else:
            content["articles"][0]["content"] = text
            content["articles"][0]["name"] = name
        return content
    except json.JSONDecodeError as e:
        sys.stderr.write(f"\n" + out.text + "\n\n")
        sys.stderr.write("Error decoding JSON\n")
        # print trace to stderr
        sys.stderr.write(f"Error: {e}\n")
        return None
    
UNTOUCHABLE_ARTICLES = ['Levadas']

def run(text):
    out = []
    articles = load_articles(text)
    long_articles_count = len([article for article in articles if len(article["body"]) >= ARTICLE_SIZE_THRESHOLD])
    lc = 0
    for i in range(len(articles)):
        article = articles[i]
        if len(article["body"]) >= ARTICLE_SIZE_THRESHOLD and article["title"] not in UNTOUCHABLE_ARTICLES:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            sys.stderr.write(f"\n{timestamp}: Article  #{i} {lc}/{long_articles_count} '{article["title"]}'\n")
            article_info = get_article_count(article["title"], article["body"])
            article_info["original_name"] = article["title"]
            lc += 1
        else:
            # continue
            article_info = {
                "original_name": article["title"],
                "reason": "Article is small, keeping everything as it is",
                "articles": [
                    {
                        "name": article["title"],
                        "content": article["body"],
                    }
                ]
            }
        # normalize_newlines
        # for article in article_info["articles"]:
            # article["content"] = normalize_newlines(article["content"])
        out.append(article_info)
    return dump_yaml(out)

def main():
    text = sys.stdin.read()
    file_name = sys.argv[1]
    out = run(text)
    with open(file_name, "w") as f:
        f.write(out)

if __name__ == "__main__":
    main()