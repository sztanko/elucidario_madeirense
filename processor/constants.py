START_INDICATOR = "<!-- START -->\n"
END_INDICATOR = "<!-- END -->\n"
ARTICLE_SEPARATOR = "<!-- ARTICLE -->\n"


def exrtract_articles_from_html(html_file):
    with open(html_file, "r") as f:
        html_string = f.read()
        articles = html_string.split(START_INDICATOR)[1].split(END_INDICATOR)[0].split(ARTICLE_SEPARATOR)
        return articles
