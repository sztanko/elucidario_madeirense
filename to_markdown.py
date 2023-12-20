import os
import json
import re
from pathlib import Path
import typer

from processor.constants import extract_articles_from_html
from processor.llm.processors.layout import LayoutProcessor
from processor.llm.processors.layout_body import LayoutBodyProcessor
from processor.llm.submitter import Submitter


DEFAULT_MESSAGE_SIZE_THRESHOLD = 10000


def extract_id_from_html(html_str):
    # <div class="article" id="a_395">
    id = re.match(r'<div class="article" id="a_(\d+)"', html_str).group(1)
    return int(id)


def main(
    html_file: Path = typer.Argument(
        ..., exists=True, file_okay=True, dir_okay=False, readable=True, resolve_path=True
    ),
    filter_by="",
    only_missing: bool = False,
    skip_validation: bool = False,
    message_size_threshold: int = DEFAULT_MESSAGE_SIZE_THRESHOLD,
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
    if only_missing:
        print("Loading articles from output dir to see what is not missing")
        existing = [json.loads(f.read_text()) for f in output_dir.glob("*.json")]
        existing_ids = set([int(a["id"]) for a in existing])
        article_subset = [a for a in article_subset if extract_id_from_html(a) not in existing_ids]

    merged = "\n".join(article_subset)
    print(f"Total articles: {len(article_subset)}, {len(merged)} chars")

    processor = LayoutProcessor(strict_validation=not skip_validation)
    submitter = Submitter(processor, message_size_threshold, "errors/layout")

    markup_list = submitter.submit_articles(article_subset)
    for markup in markup_list:
        index = markup["id"]
        # filename = f"articles/{index}_{re.sub('[^a-zA-Z0-9]', '_', markup['title'])}.json"
        filename = output_dir / f"{index}_{markup['title']}.json"
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
