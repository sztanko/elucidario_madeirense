import sys
from bs4 import BeautifulSoup, NavigableString, Tag
import re
from pyuca import Collator
import tty
import termios
import json

from processor.journal import Journal

ADJUST_JOURNAL_FILE = "journals/adjust_journal.json"
INPUT_DIR = "html"

ROMAN_NUMERALS = [
    "I ",
    "II ",
    "III ",
    "IV ",
    "V ",
    "VI ",
    "VII ",
    "VIII ",
    "IX ",
    "X ",
    "XI ",
    "XII ",
    "XIII",
    "XIV",
    "XV",
    "XVI",
    "XVII",
    "XVIII",
    "XIX",
    "XX ",
    "XXI",
    "XXII",
    "XXIII",
    "XXIV",
    "XXV",
    "XXVI",
    "XXVII",
    "XXVIII",
]

FILES = [f"{INPUT_DIR}/vol_{i}_cleaned.html" for i in range(1, 4)]

adjust_journal = Journal(ADJUST_JOURNAL_FILE)


def join_files(files):
    content = []
    for file in files:
        with open(file, "r") as f:
            soup = BeautifulSoup(f.read(), "html.parser")
            # all element in body to be appended to content
            for el in soup.body.contents:
                content.append(el)
    return content


def group_articles(tags):
    i = 0
    articles = []
    print(f"Length of tags: {len(tags)}")
    while i < len(tags):
        tag = tags[i]
        if tag.name == "b":
            article = {}
            title = tag.text.strip()
            article["title"] = title
            # print(title)
            i += 1
            body = []
            html = []
            while i < len(tags) and tags[i].name != "b":
                txt = tags[i].text.strip()
                # print(txt)
                body.append(txt)
                html.append(tags[i])
                i += 1
            article["body"] = body
            article["html"] = html
            articles.append(article)
        else:
            # print(tag.name)
            # print(i)
            i += 1
    print(f"Count of artciles: {len(articles)}")
    return articles


def adjust_articles(articles):
    collator = Collator()
    # All articles should be alphabetically ordered. If an article is not between it's neighbours, it is a mistake and it should be just a part of the body of the previoys artcile
    out = [articles[0]]
    i = 1
    while i < len(articles) - 1:
        title = articles[i]["title"]
        last_article = out[-1]
        previous_decision = adjust_journal.in_journal(i, title)
        if previous_decision is not None:
            should_merge = previous_decision
            # if should_merge:
            #    print(f"Article will be merged with {last_article['title']}")
        else:
            # print(f"Checking article {title} ({i}/{len(articles)})")
            should_merge = False
            if any([title.startswith(rn) for rn in ROMAN_NUMERALS]):
                # print(f"Previous article:\t{last_article['title']}:\t{str(last_article['body'])[0:100] }")
                # print(f"Current  article:\t{title}:\t{str(articles[i]['body'])[0:100] }")
                # print(f"Next     article:\t{articles[i+1]['title']}\t{str(articles[i+1]['body'])[0:100] }")
                # print("Article starts with Roman numberals, it is probably a reference to another article. Ask user")
                should_merge = adjust_journal.ask_if_merge(i, articles[i]["title"])
            elif (title.startswith("V. ") or title.startswith("Vid.")) and not last_article["title"].startswith("V"):
                # print("Article starts with 'V. ' or 'Vid.', it is probably a reference to another article. Merge")
                should_merge = True
            elif title.startswith(")"):
                # print("Article starts with ')', it is just enclosure of the previous title. Merge")
                should_merge = True
            elif collator.sort_key(title) < collator.sort_key(last_article["title"]) or collator.sort_key(
                title
            ) > collator.sort_key(articles[i + 1]["title"]):
                # print("\n")
                # print(f"Previous article:\t{last_article['title']}:\t{str(last_article['body'])[0:100] }")
                # print(f"Current  article:\t{title}:\t{str(articles[i]['body'])[0:100] }")
                # print(f"Next     article:\t{articles[i+1]['title']}\t{str(articles[i+1]['body'])[0:100] }")
                # print(f"{i} / {len(articles)} ------------------\n")
                # print(f"Article {articles[i]['title']} is not between it's neighbours, it is a mistake and it should be just a part of the body of the previoys artcile")
                if title[0:2] == last_article["title"][0:2]:
                    # print("Article has similar beginning, safe to keep separate")
                    should_merge = False
                else:
                    should_merge = adjust_journal.ask_if_merge(i, articles[i]["title"])

        # if not should_merge:
        #     print(f"'S'. Article {articles[i]['title']} will be split (kept) as a standalone article")
        #     print()
        if should_merge:
            header = Tag(name="h2")
            header.string = articles[i]["title"]
            last_article["body"].append(articles[i]["title"])
            last_article["html"].append(header)
            last_article["body"].extend(articles[i]["body"])
            last_article["html"].extend(articles[i]["html"])
            # print(f"'Y'. Article {articles[i]['title']} will be merged with previous article")
            # print()
            out[-1] = last_article
        else:
            out.append(articles[i])
        i += 1
    out.append(articles[-1])
    adjust_journal.save()
    return out


def detect_article(collator, article, next_name):
    # These articles are still part of the previous article, they should be split.
    # Checked manually.
    SKIP_SPLIT_LIST = [
        "Não foi necessário tamanho sacrifício",
        "Morreu Henrique Henriques de Noronha a 26 de Abril de 1730",
    ]
    tag_spec = [(False, "br"), (True, "\n"), (False, "br")]
    prev_name = article["title"]
    # new_articles = []
    line_num = 0
    for line in article["html"]:
        # print(line)
        if isinstance(line, NavigableString):
            line_num += 1
            continue
        content = line.contents
        i = 3  # It always should be the third tag
        if len(content) > 3:
            # while i < len(content):
            j = 0
            tag_match = True
            while j < len(tag_spec) and tag_match:
                c = content[i - len(tag_spec) + j]
                is_str = isinstance(c, NavigableString)
                if is_str:  # this is a text
                    text = c
                else:  # this is tag
                    text = c.name
                spec = tag_spec[j]
                if not (is_str == spec[0] and text == spec[1]):
                    tag_match = False
                    break
                j += 1
            if tag_match and isinstance(content[i], NavigableString):
                sentences = re.split(r"\.\s+", content[i].strip())
                if len(sentences) > 1:
                    title = sentences[0].strip()
                    if (
                        collator.sort_key(prev_name) < collator.sort_key(title)
                        and collator.sort_key(title) < collator.sort_key(next_name)
                        and title not in SKIP_SPLIT_LIST
                    ):
                        print(f"Found article {title}, inside article {article['title']}")
                        print(i)
                        new_article = {"title": title, "line": line_num, "i": i}
                        print(new_article)
                        articles = split_article(article, new_article)
                        return articles
                        # new_articles.append(new_article)
            # i += 1
        line_num += 1
    return [article]


def split_article(article, new_article_info):
    new_article = {}
    new_article["title"] = new_article_info["title"]
    new_article["body"] = article["body"][new_article_info["line"] :]
    new_article["html"] = article["html"][new_article_info["line"] :]
    # Replace the first occurrence of the title with an empty string
    modified_html_string = str(new_article["html"][0]).replace(new_article["title"] + ".", "", 1)

    # Update the HTML content in your data structure
    new_article["html"][0] = BeautifulSoup(modified_html_string, "html.parser")
    # print(new_article["html"])
    article["body"] = article["body"][0 : new_article_info["line"]]
    article["html"] = article["html"][0 : new_article_info["line"]]
    return [article, new_article]


def split_articles(articles):
    collator = Collator()
    out = []
    i = 0
    for article in articles:
        if i == 0:
            next_name = articles[i + 1]["title"]
        else:
            next_name = "zzzzzzzz"
        out.extend(detect_article(collator, article, next_name))
        i += 1
    return out


def write_articles(articles, output_file_name):
    # Each article should be enclosed in a div, title should be an H1 tag, and the body should be enclosed in a <div className="article-body">"
    with open(output_file_name, "w") as f:
        f.write("<html><body>")
        i = 0
        for article in articles:
            f.write(f"<div className='article' id='a_{i}'>\n<h1>{article['title']}</h1>\n\n")
            f.write("<div className='article-body'>\n")
            for line in article["html"]:
                if isinstance(line, NavigableString):
                    f.write(line)
                else:
                    f.write(line.prettify())
            f.write("\n</div>\n</div>\n")
            i += 1
        f.write("</body></html>")


def show_article_stats(articles):
    from collections import Counter

    words = Counter()
    chars = Counter()
    for article in articles:
        # print(f"{article['title']}: {len(article['body'])}")
        total_chars = sum([len(line) for line in article["body"]])
        # split by regex
        total_words = sum([len(re.split(r"\s+", line)) for line in article["body"]])
        words[1000 * int(total_words / 1000)] += 1
        chars[1000 * int(total_chars / 1000)] += 1
    print(words)
    print(chars)


def find_max_length(articles):
    max_length = 0
    art = None
    for article in articles:
        total_chars = sum([len(line) for line in article["body"]])
        if total_chars > max_length:
            max_length = total_chars
            art = article["title"]
    print(f"Max length: {max_length} for {art}")
    return max_length


def remove_new_lines_in_text(text):
    text = re.sub(r"\s*\n+", " ", text)
    return text


def write_lengths_to_csv(articles):
    with open("lengths.csv", "w") as f:
        f.write(f"title\tseq\twords\tchars\n")
        i = 0
        for article in articles:
            total_chars = sum([len(line) for line in article["body"]])
            total_words = sum([len(re.split(r"\s+", line)) for line in article["body"]])
            title = remove_new_lines_in_text(article["title"]).strip()
            f.write(f"{title}\t{i}\t{total_words}\t{total_chars}\n")
            i += 1


def run(output_file_name):
    content = join_files(FILES)
    articles = group_articles(content)
    articles = adjust_articles(articles)
    articles = split_articles(articles)
    write_articles(articles, output_file_name)
    # show_article_stats(articles)
    # find_max_length(articles)
    # write_lengths_to_csv(articles)


if __name__ == "__main__":
    run(sys.argv[1])
