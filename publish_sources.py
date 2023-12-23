import os
import json
from pathlib import Path
import typer
import logging
from processor.constants import CATEGORY_MAP

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(filename)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()],
)


def post_process(markup):
    pass


def cap(s: str):
    return s[0].upper() + s[1:] if s else s


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
):
    # load all json files located in articles_path
    assert articles_path != output_path
    assert translations_path != output_path
    logging.info("Reading articles from %s", articles_path)
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
                    "body": cap(a["body"]),
                    "people": {k: cap(v) for k, v in a.get("people", {}).items()},
                    "locations": {k: cap(v) for k, v in a.get("locations", {}).items()},
                    "years": {k: cap(v) for k, v in a.get("years", {}).items()},
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
                "body": cap(translation["body"]),
                "people": {k: cap(v) for k, v in translation.get("people", {}).items()},
                "locations": {k: cap(v) for k, v in translation.get("locations", {}).items()},
                "years": {k: cap(v) for k, v in translation.get("years", {}).items()},
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
        os.makedirs(lang_path, exist_ok=True)
        index = []
        for id, article in article_map.items():
            item = {
                "id": id,
                "title": article["translations"][lang]["title"],
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
            article = {
                "id": id,
                "lang": lang,
                "is_original": lang == "pt",
                "title": article["translations"][lang]["title"],
                "original_title": article["translations"]["pt"]["title"],
                "body": article["translations"][lang]["body"],
                "categories": [CATEGORY_MAP[c] for c in article["categories"]],
                "freguesias": article["freguesias"],
                "locations": article["translations"][lang]["locations"],
                "people": article["translations"][lang]["people"],
                "years": article["translations"][lang]["years"],                
            }
            
            filename = lang_path / f"{id}.json" 
            with open(filename, "w") as f:
                # logging.info(f"Writing to {filename}")
                json.dump(article, f, indent=4, ensure_ascii=False)
        # Sort index by title
        index = sorted(index, key=lambda x: x["title"])
        
        index_filename = output_path / f"index_{lang}.json"
        with open(index_filename, "w") as f:
            # logging.info(f"Writing to {filename}")
            json.dump(index, f, indent=4, ensure_ascii=False)
            logging.info(f"Written {len(index)} articles to index {index_filename}")
    

if __name__ == "__main__":
    import sys

    typer.run(main)
