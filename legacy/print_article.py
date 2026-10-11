import json


def print_article(data):
    # print("# Title:\t" + data["title"])
    # print(f"*Length:*\t{len(data['body'])} characters, {len(data['body'].split())} words")
    # print()
    # print("*References:*\t" + ", ".join(data["references"]))
    # print()
    # print("*Categories:*\t" + ", ".join(data["categories"]))
    # print()
    print(data["body"])
    # print("------------------------------------------------------")


def main(article_file):
    with open(article_file, "r") as f:
        data = json.load(f)
        if isinstance(data, dict):
            print_article(data)
        else:
            for article in data:
                print_article(article)
            print(f"Total articles: {len(data)}")


if __name__ == "__main__":
    import os
    import sys

    if len(sys.argv) != 2:
        print("Usage: python print_article.py <article_file>")
        sys.exit(1)
    if not os.path.exists(sys.argv[1]):
        print(f"Error: file '{sys.argv[1]}' not found")
        sys.exit(1)
    main(sys.argv[1])
