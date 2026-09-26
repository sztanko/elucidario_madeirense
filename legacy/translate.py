from typing import Optional
import json
import re
from pathlib import Path
import typer

from processor.llm.processors.translation import TranslationProcessor
from processor.llm.submitter import Submitter


DEFAULT_MESSAGE_SIZE_THRESHOLD = 6000


def main(
    lang: str,
    articles_path: Path = typer.Argument(
        ..., exists=True, file_okay=False, dir_okay=True, readable=True, resolve_path=True
    ),
    output_dir: Path = typer.Argument(
        ...,
        exists=True,
        file_okay=False,
        dir_okay=True,
        readable=True,
        resolve_path=True,
    ),
    only_missing: bool = False,
    filter_by="",
    message_size_threshold: int = DEFAULT_MESSAGE_SIZE_THRESHOLD,
    engine: Optional[str] = None,
):
    # load all json files located in articles_path
    print("Reading articles")
    articles = [json.loads(f.read_text()) for f in articles_path.glob("*.json")]
    print(f"Loaded {len(articles)} articles")
    if only_missing:
        print("Loading articles from output dir to see what is not missing")
        existing = [json.loads(f.read_text()) for f in output_dir.glob("*.json")]
        existing_ids = set([int(a["id"]) for a in existing])
        print(f"Existing ids: {len(existing_ids)}")
        article_subset = [a for a in articles if int(a["id"]) not in existing_ids]
        if len(article_subset) < 50:
            for a in article_subset:
                print(f"Missing: {a['id']} - {a['title']}")
    article_subset = list(filter(lambda a: a["title"].startswith(filter_by), article_subset))
    merged_articles = [json.dumps(a, ensure_ascii=False) for a in article_subset]
    # print(merged_articles)
    print(f"Total articles: {len(article_subset)}, {sum([len(a) for a in merged_articles])} chars")

    processor = TranslationProcessor(lang, engine_str=engine)
    submitter = Submitter(processor, message_size_threshold, f"errors/translation/{lang}")

    markup_list = submitter.submit_articles(merged_articles)
    for markup in markup_list:
        index = markup["id"]
        # filename = f"articles/{index}_{re.sub('[^a-zA-Z0-9]', '_', markup['title'])}.json"
        filename = output_dir / f"{index}_{lang}_{markup['title']}.json"
        with open(filename, "w") as f:
            print(f"Writing to {filename}")
            json.dump(markup, f, indent=4, ensure_ascii=False)
        print(f"This is article #{index}")
    print("FInished all articles")


if __name__ == "__main__":
    import sys

    typer.run(main)
