import os
import json
import re

from processor.constants import exrtract_articles_from_html
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


def main(html_file, filter_by):
    articles = exrtract_articles_from_html(html_file)
    # filter_by = "Indústria Vinícola"
    # filter_by = "Ingleses"
    # filter_by = "Insubordinações Militares"
    # filter_by = "Levadas"
    # filter_by = "Terreiro da Luta"
    # filter_by = "Madeira e a«Ilha dos Amores»"
    # filter_by = "Prostituição"
    # filter_by = "Bancos"
    # filter_by = "Colegio. V. São João Evangelista (Colegio e igreja de)"
    # filter_by = "Calheta"
    # filter_by = "Rodrigues ("
    # filter_by = "Ab"
    # filter_by = "Baleira (Vi"
    # filter_by = "Silva"
    article_subset = list(filter(lambda a: f">{filter_by}" in a, articles))
    merged = "\n".join(article_subset)
    print(f"Total articles: {len(article_subset)}, {len(merged)} chars")
    processor = ArticleProcessor()
    markup_list = processor.submit_multiple_articles(article_subset)
    for markup in markup_list:
        # markup = processor.submit_article(a)
        print(markup)
        index = markup["id"]
        filename = f"articles/{index}_{re.sub('[^a-zA-Z0-9]', '_', markup['title'])}.json"
        with open(filename, "w") as f:
            print(f"Writing to {filename}")
            json.dump(markup, f, indent=4, ensure_ascii=False)
        print(f"This if article #{index}")
        a = articles[index]
        similarity_score = get_similarity_score(a, markup["body"])
        print("Similarity score: " + str(similarity_score))


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 3:
        print("Usage: python to_json.py <html_file> article_name")
        sys.exit(1)
    if not os.path.exists(sys.argv[1]):
        print(f"Error: file '{sys.argv[1]}' not found")
        sys.exit(1)
    main(sys.argv[1], sys.argv[2])
