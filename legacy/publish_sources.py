from typing import Dict, List

import os
import json
from pathlib import Path
import typer
import logging
import re
from processor.constants import CATEGORY_MAP

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(filename)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()],
)


def get_first_letter(s: str):
    # get first alphanumerical character
    for c in s:
        if c.isalnum():
            return c


def post_process(markup):
    replacements = {
        "\n\n##\n\n": "\n\n##",
        "\\n": "\n",
        "{": "",
        "}": "",
    }
    regexps = (
        (r"(#+)(?=[^#\s])", lambda m: "#" * len(m.group(1))),
        # if there is \n\n followed by a small letter, replace \n\n with space
        (r"(\n\n)(?=[a-z])", lambda m: " "),
    )
    for k, v in replacements.items():
        markup = markup.replace(k, v)
    for regexp, repl in regexps:
        markup = re.sub(regexp, repl, markup)
    return markup


def cap(s: str):
    return s[0].upper() + s[1:] if s else s


def pr_cats(cats: Dict[str, str]) -> Dict[str, List[str]]:
    # split values by "\n\n"
    out = {}
    for k, v in cats.items():
        out[cap(k)] = [cap(c.strip()) for c in post_process(v).split("\n\n")]
    return out


def main(
    articles_path: Path = typer.Argument(
        ..., exists=True, file_okay=False, dir_okay=True, readable=True, resolve_path=True
    ),
    translations_path: Path = typer.Argument(
        ..., exists=True, file_okay=False, dir_okay=True, readable=True, resolve_path=True
    ),
    output_path: Path = typer.Argument(
        ..., file_okay=False, dir_okay=True, readable=True, writable=True, resolve_path=True
    ),
    web_path: Path = typer.Argument(
        ..., file_okay=False, dir_okay=True, readable=True, writable=True, resolve_path=True, exists=True
    ),
):
    # load all json files located in articles_path
    assert articles_path != output_path
    assert translations_path != output_path
    assert output_path != web_path
    logging.info("Reading articles from %s", articles_path)
    logging.info(f"Web path is {web_path}")
    articles = [json.loads(f.read_text()) for f in articles_path.glob("*.json")]
    for article in articles:
        for k in ["freguesias", "categories", "references"]:
            if k not in article or article[k] is None:
                article[k] = []
        for k in ["people", "locations", "years"]:
            if k not in article or article[k] is None:
                article[k] = {}
    article_map = {
        a["id"]: {
            "id": a["id"],
            "categories": [cap(c) for c in a["categories"] if a["categories"]],
            "references": a["references"],
            "freguesias": [cap(f) for f in a.get("freguesias", [])],
            "translations": {
                "pt": {
                    "title": cap(a["title"]),
                    "body": post_process(cap(a["body"])),
                    "people": pr_cats(a.get("people", {})),
                    "locations": pr_cats(a.get("locations", {})),
                    "years": pr_cats(a.get("years", {})),
                }
            },
        }
        for a in articles
    }
    # translation path has actually a series of subpaths, each is a language code, like de, fr, etc
    # each of these subpaths has a series of json files, each is a translation of an article
    available_langs = []
    for lang_path in translations_path.glob("*"):
        lang = lang_path.name
        available_langs.append(lang)
        logging.info(f"Processing language {lang}")
        for translation_file in lang_path.glob("*.json"):
            translation = json.loads(translation_file.read_text())
            article_id = translation["id"]
            for k in ["people", "locations", "years"]:
                if k not in translation or translation[k] is None:
                    translation[k] = {}
            translation_obj = {
                "title": cap(translation["title"]),
                "body": post_process(cap(translation["body"])),
                "people": pr_cats(translation.get("people", {})),
                "locations": pr_cats(translation.get("locations", {})),
                "years": pr_cats(translation.get("years", {})),
            }
            article_map[article_id]["translations"][lang] = translation_obj
    logging.info(f"Loaded {len(articles)} articles")

    # Create output dir, if doesn't exist
    # We need to create:
    # 1. Index file, for each language
    # 2. Article files, for each language

    os.makedirs(output_path, exist_ok=True)
    logging.info(f"Writing to {output_path}")
    # 1. Create index files:

    for lang in available_langs + ["pt"]:
        # Create a directory under output_path for each language
        lang_path = output_path / lang
        ebook_path = output_path / "ebook"
        ebook_path_lang = output_path / "ebook" / lang
        os.makedirs(lang_path, exist_ok=True)
        os.makedirs(ebook_path_lang, exist_ok=True)
        # full_book = EpubWriter("full", lang, f"Elucidario Madeirense {lang}")
        index = []
        full_index = []
        for id, article in article_map.items():
            item = {
                "id": id,
                "title": article["translations"][lang]["title"] or article["translations"]["pt"]["title"],
                "fl": get_first_letter(article["translations"][lang]["title"]),
                "original_title": article["translations"]["pt"]["title"],
                "categories": [CATEGORY_MAP[c] for c in article["categories"]],
                "freguesias": article["freguesias"],
                "locations": list(article["translations"][lang]["locations"].keys()),
                "people": list(article["translations"][lang]["people"].keys()),
                "years": list(article["translations"][lang]["years"].keys()),
                "length": len(article["translations"][lang]["body"]),
                "is_original": lang == "pt",
            }
            index.append(item)
            art = {
                "id": id,
                "lang": lang,
                "is_original": lang == "pt",
                "title": article["translations"][lang]["title"],
                "fl": get_first_letter(article["translations"][lang]["title"]),
                "original_title": article["translations"]["pt"]["title"],
                "body": article["translations"][lang]["body"],
                "categories": [CATEGORY_MAP[c] for c in article["categories"]],
                "freguesias": article["freguesias"],
                "locations": article["translations"][lang]["locations"],
                "people": article["translations"][lang]["people"],
                "years": article["translations"][lang]["years"],
            }
            full_index.append(art)
            # book = EpubWriter(id, lang, article["title"])
            # book.add_chapter(article["title"], article["body"])
            # full_book.add_chapter(article["title"], article["body"])
            filename = lang_path / f"{id}.json"
            with open(filename, "w") as f:
                # logging.info(f"Writing to {filename}")
                json.dump(art, f, indent=4, ensure_ascii=False)
            # book.generate_toc()
            # book.write_book(ebook_path / lang / f"{id}.epub")
        # Sort index by title
        index = sorted(index, key=lambda x: x["title"])

        index_filename = output_path / f"index_{lang}.json"
        with open(index_filename, "w") as f:
            # logging.info(f"Writing to {filename}")
            json.dump(index, f, indent=4, ensure_ascii=False)
            logging.info(f"Written {len(index)} articles to index {index_filename}")
        index_filename_web = web_path / f"index_{lang}.json"
        with open(index_filename_web, "w") as f:
            # logging.info(f"Writing to {filename}")
            json.dump(index, f, ensure_ascii=False)
            logging.info(f"Written {len(index)} articles to index {index_filename_web}")

        full_index_filename = web_path / f"index_full_{lang}.json"
        with open(full_index_filename, "w") as f:
            # logging.info(f"Writing to {filename}")
            json.dump(full_index, f, ensure_ascii=False)
            logging.info(f"Written {len(full_index)} articles to index {full_index_filename}")
        # full_book.generate_toc()
        # full_book.write_book(ebook_path / f"elucidario_madeirense_{lang}.epub")


if __name__ == "__main__":
    import sys

    typer.run(main)
