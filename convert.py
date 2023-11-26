import sys
from bs4 import BeautifulSoup, NavigableString
import re
from pyuca import Collator
import tty
import termios
import json

INPUT_DIR = "html"

ROMAN_NUMERALS = ['I ', 'II ', 'III ', 'IV ', 'V ', 'VI ', 'VII ', 'VIII ', 'IX ', 'X ', 'XI ', 'XII ', 'XIII', 'XIV', 'XV', 'XVI', 'XVII', 'XVIII', 'XIX', 'XX ', 'XXI', 'XXII', 'XXIII', 'XXIV', 'XXV', 'XXVI', 'XXVII', 'XXVIII']

FILES = [f"{INPUT_DIR}/vol_{i}_cleaned.html" for i in range(1, 4)]
ADJUST_JOURNAL_FILE = "journals/adjust_journal.json"

adjust_journal = {}

def read_key():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        key = sys.stdin.read(1)
    except KeyboardInterrupt:
        return 'Ctrl-C'
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return key

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
    while i<len(tags):
        tag = tags[i]
        if tag.name == 'b':
            article = {}
            title = tag.text.strip()
            article['title'] = title
            # print(title)
            i += 1
            body = []
            html = []
            while i<len(tags) and tags[i].name != 'b':
                txt = tags[i].text.strip()
                # print(txt)
                body.append(txt)
                html.append(tags[i])
                i += 1
            article['body'] = body
            article['html'] = html
            articles.append(article)
        else:
            # print(tag.name)
            # print(i)
            i += 1
    print(f"Count of artciles: {len(articles)}")
    return articles

def ask_if_merge(i, term):
    global adjust_journal
    previous_decision = in_adjust_journal(i, term)
    if previous_decision is not None:
        return previous_decision
    print("Press 'm' to merge with previous article, 's' to split it as a standalone article, or c to cancel")    
    key = read_key()
    while key not in ['m', 's', 'c']:
        key = read_key()
    if key == 'Ctrl-C' or key == 'c':
        print("Cancelling")
        save_adjust_journal()
        sys.exit(1)
    log_adjust_journal(i, term, key)
    return key == 'm'

def in_adjust_journal(i, term):
    global adjust_journal
    if i in adjust_journal:
        if adjust_journal[i]['term'] != term:
            raise Exception(f"Term {term} is not the same as {adjust_journal[i]['term']}. Looks like adjust jounral is corrupted")
        # print(f"Article {adjust_journal[i]['term']} was already adjusted to {adjust_journal[i]['decision']}")
        return adjust_journal[i]['decision'] == 'm'
    return None

def log_adjust_journal(i, term, decision):
    global adjust_journal
    print("logging the decision")
    out = {'i': i, 'term': term, 'decision': decision}
    print(out)
    adjust_journal[i] = out

def save_adjust_journal():
    global adjust_journal
    print("Saving journal...")
    with open(ADJUST_JOURNAL_FILE, "w") as f:
        f.write(json.dumps(adjust_journal, indent=2))
    print(f"Saved {len(adjust_journal)} decisions")

def load_adjust_journal():
    global adjust_journal
    c = 0
    with open(ADJUST_JOURNAL_FILE, "r") as f:
        adjust_journal_str = json.loads(f.read())
        for (k,v) in adjust_journal_str.items():
            adjust_journal[int(k)] = v
            c+=1
    print(f"Loaded {c} decisions")        
    

def adjust_articles(articles):
    collator = Collator()
    load_adjust_journal()
    # All articles should be alphabetically ordered. If an article is not between it's neighbours, it is a mistake and it should be just a part of the body of the previoys artcile
    out = [articles[0]]
    i = 1
    while i < len(articles)-1:
        title = articles[i]['title']
        last_article = out[-1]
        previous_decision = in_adjust_journal(i, title)
        if previous_decision is not None:
            should_merge = previous_decision
            #if should_merge:
            #    print(f"Article will be merged with {last_article['title']}")
        else:    
            # print(f"Checking article {title} ({i}/{len(articles)})")
            should_merge = False
            if any([title.startswith(rn) for rn in ROMAN_NUMERALS]):
                # print(f"Previous article:\t{last_article['title']}:\t{str(last_article['body'])[0:100] }")
                # print(f"Current  article:\t{title}:\t{str(articles[i]['body'])[0:100] }")
                # print(f"Next     article:\t{articles[i+1]['title']}\t{str(articles[i+1]['body'])[0:100] }")
                # print("Article starts with Roman numberals, it is probably a reference to another article. Ask user")
                should_merge = ask_if_merge(i, articles[i]['title'])
            elif (title.startswith("V. ") or title.startswith("Vid.")) and not last_article['title'].startswith("V"):
                    # print("Article starts with 'V. ' or 'Vid.', it is probably a reference to another article. Merge")
                    should_merge = True
            elif title.startswith(")"):
                    # print("Article starts with ')', it is just enclosure of the previous title. Merge")
                    should_merge = True 
            elif collator.sort_key(title) < collator.sort_key(last_article['title']) or collator.sort_key(title) > collator.sort_key(articles[i+1]['title']):                                        
                # print("\n")                       
                # print(f"Previous article:\t{last_article['title']}:\t{str(last_article['body'])[0:100] }")
                # print(f"Current  article:\t{title}:\t{str(articles[i]['body'])[0:100] }")
                # print(f"Next     article:\t{articles[i+1]['title']}\t{str(articles[i+1]['body'])[0:100] }")
                # print(f"{i} / {len(articles)} ------------------\n") 
                # print(f"Article {articles[i]['title']} is not between it's neighbours, it is a mistake and it should be just a part of the body of the previoys artcile") 
                if title[0:2] == last_article['title'][0:2]:
                    # print("Article has similar beginning, safe to keep separate")
                    should_merge = False
                else:
                    should_merge = ask_if_merge(i, articles[i]['title'])
        
        # if not should_merge:
        #     print(f"'S'. Article {articles[i]['title']} will be split (kept) as a standalone article")
        #     print()
        if should_merge:
            last_article['body'].append(f"<h2>{articles[i]['title']}</h2>")
            last_article['body'].extend(articles[i]['body'])
            # print(f"'Y'. Article {articles[i]['title']} will be merged with previous article")
            # print()
            out[-1] = last_article            
        else:
            out.append(articles[i])
        i+=1
    out.append(articles[-1])
    save_adjust_journal()
    return out

def extract_articles(article, next_article_name):
    # Within each artcile, lets seek for the following patterns:
    # <br/></span><span><br/>
    # <br/>
    # ([A-Z][a-z ]+)\.
    # if group(1) is larger then the article name and smaller then the next article name, then it is probably an article as well, and should become separate
    
    out = []
    content = article['body']
    i=0
    while i<len(content):
        if content[i] == '':
            i += 1
            continue
        if content[i] == '<br/>':
            i += 1
            continue
        if content[i].startswith('<br/></span><span><br/>'):
            i += 1
            continue
        if content[i].startswith('<span><br/>'):
            i += 1
            continue
        if content[i].startswith('<br/><span>'):
            i += 1
            continue
        if content[i].startswith('<span>'):
            i += 1
            continue
        if content[i].startswith('<br/>'):
            i += 1
            continue
        m = re.match(r"([A-Z][a-z ]+)\.", content[i])
        if m:
            if article['title'] < m.group(1) < next_article_name:
                out.append({'title': m.group(1), 'body': []})
                i += 1
                continue
        out[-1]['body'].append(content[i])
        i += 1

def write_articles(articles, output_file_name):    
    # Each article should be enclosed in a div, title should be an H1 tag, and the body should be enclosed in a <div className="article-body">"
    with open(output_file_name, "w") as f:
        f.write("<html><body>")
        i = 0
        for article in articles:
            f.write(f"<div className='article' id='a_{i}'>\n<h1>{article['title']}</h1>\n\n")
            f.write("<div className='article-body'>\n")
            for line in article['html']:
                if isinstance(line, NavigableString):
                    f.write(line)
                else:
                    f.write(line.prettify())            
            f.write("\n</div>\n</div>\n")
            i+=1
        f.write("</body></html>")            

def show_article_stats(articles):
    from collections import Counter
    words = Counter()
    chars = Counter()
    for article in articles:
        #print(f"{article['title']}: {len(article['body'])}")
        total_chars = sum([len(line) for line in article['body']])
        # split by regex
        total_words = sum([len(re.split(r"\s+", line)) for line in article['body']])
        words[1000*int(total_words/1000)] += 1
        chars[1000*int(total_chars/1000)] += 1
    print(words)
    print(chars)

def find_max_length(articles):
    max_length = 0
    art = None
    for article in articles:
        total_chars = sum([len(line) for line in article['body']])
        if total_chars > max_length:
            max_length = total_chars
            art = article['title']
    print(f"Max length: {max_length} for {art}")
    return max_length

def remove_new_lines_in_text(text):
    text = re.sub(r"\s*\n+", " ", text)
    return text

def write_lengths_to_csv(articles):
    with open("lengths.csv", "w") as f:
        f.write(f"title\tseq\twords\tchars\n")
        i=0
        for article in articles:
            total_chars = sum([len(line) for line in article['body']])
            total_words = sum([len(re.split(r"\s+", line)) for line in article['body']])
            title = remove_new_lines_in_text(article['title']).strip()
            f.write(f"{title}\t{i}\t{total_words}\t{total_chars}\n")
            i+=1

def run(output_file_name):
    content = join_files(FILES)
    articles = group_articles(content)
    articles = adjust_articles(articles)
    write_articles(articles, output_file_name)
    # show_article_stats(articles)
    # find_max_length(articles)
    # write_lengths_to_csv(articles)
    
if __name__ == "__main__":
    run(sys.argv[1])