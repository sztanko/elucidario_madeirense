import os
import json
import re
from pathlib import Path
import typer

from processor.constants import extract_articles_from_html
from processor.constants import (
    DEFAULT_INSTRUCTIONS_FILE,
    DEFAULT_SIMPLE_GPT_MODEL,
    DEFAULT_COMPLEX_GPT_MODEL,
    DEFAULT_MESSAGE_SIZE_THRESHOLD,
)
from processor.ai import ArticleProcessor
from processor.normalizer import get_similarity_score


def print_article(data):
    print("Title:\t" + data["title"])
    print(f"Length:\t{len(data['body'])} characters, {len(data['body'].split())} words")
    print("References:\t" + ", ".join(data["references"]))
    print("Categories:\t" + ", ".join(data["categories"]))
    print()
    print(data["body"])
    print("------------------------------------------------------")


def main(
    html_file: Path = typer.Argument(
        ..., exists=True, file_okay=True, dir_okay=False, readable=True, resolve_path=True
    ),
    filter_by="",
    instructions_file=DEFAULT_INSTRUCTIONS_FILE,
    message_size_threshold: int = DEFAULT_MESSAGE_SIZE_THRESHOLD,
    simple_gpt_model=DEFAULT_SIMPLE_GPT_MODEL,
    complex_gpt_model=DEFAULT_COMPLEX_GPT_MODEL,
    output_dir: Path = typer.Option(
        "articles",
        exists=True,
        file_okay=False,
        dir_okay=True,
        readable=True,
        resolve_path=True,
    ),
):
    articles = extract_articles_from_html(html_file)
    article_subset = list(filter(lambda a: f">{filter_by}" in a, articles))
    merged = "\n".join(article_subset)
    print(f"Total articles: {len(article_subset)}, {len(merged)} chars")
    processor = ArticleProcessor(
        instructions_file=instructions_file,
        message_size_threshold=message_size_threshold,
        simple_gpt_model=simple_gpt_model,
        complex_gpt_model=complex_gpt_model,
    )
    markup_list = processor.submit_multiple_articles(article_subset)
    for markup in markup_list:
        # markup = processor.submit_article(a)
        print(markup)
        index = markup["id"]
        # filename = f"articles/{index}_{re.sub('[^a-zA-Z0-9]', '_', markup['title'])}.json"
        filename = output_dir / f"{index}_{re.sub('[^a-zA-Z0-9]', '_', markup['title'])}.json"
        with open(filename, "w") as f:
            print(f"Writing to {filename}")
            json.dump(markup, f, indent=4, ensure_ascii=False)
        print(f"This if article #{index}")


if __name__ == "__main__":
    import sys

    typer.run(main)

    # if len(sys.argv) < 2:
    #     print("Usage: python to_json.py <html_file> article_name")
    #     sys.exit(1)

    # if not os.path.exists(sys.argv[1]):
    # print(f"Error: file '{sys.argv[1]}' not found")
    # sys.exit(1)
