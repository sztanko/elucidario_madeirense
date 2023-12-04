import os
import time
import json
from openai import OpenAI

from processor.splitter import split_article


TO_JSON_ASSISTANT_ID = "asst_5KvfwvB6nXR7QSXDo06OUqmS"

MESSAGE_SIZE_THRESHOLD = 10000

MAX_RETRIES = 3

GPT_MODEL = "gpt-3.5-turbo-1106"
# GPT_MODEL = "gpt-4-1106-preview"
INSTRUCTIONS_FILE = "instructions/to_json_ai_revised.txt"


SIMPLE_GPT_MODEL = "gpt-3.5-turbo-1106"
COMPLEX_GPT_MODEL = SIMPLE_GPT_MODEL  # "gpt-4-1106-preview"


def get_json(response):
    # print(response)
    print(f"Response length: {len(response)}")
    try:
        data = json.loads(response)
        if "a" not in data:
            print("Error: 'a' not in data")
            print(response)
            raise Exception("Error: 'a' not in data")
        if not isinstance(data["a"], list):
            print("Error: 'a' is not a list")
            print(response)
            raise Exception("Error: 'a' is not a list")
    except json.decoder.JSONDecodeError as e:
        print("Error: JSONDecodeError")
        print(response)
        raise e
    return data["a"]


def unify_chunks(chunks):
    return {
        "title": chunks[0]["title"],
        "id": chunks[0]["id"],
        "references": list(set([ref for chunk in chunks for ref in chunk.get("references") or []])),
        "categories": list(set([cat for chunk in chunks for cat in chunk.get("categories") or []])),
        "freguesias": list(set([freg for chunk in chunks for freg in chunk.get("freguesias") or []])),
        "body": "\n\n".join([chunk["body"] for chunk in chunks]),
    }


def group_articles(articles, threshold):
    groups = []
    current_group = []
    current_length = 0

    for article in articles:
        article_length = len(article)
        if article_length > threshold:
            # If the current group has articles, add it to groups
            if current_group:
                groups.append(current_group)
                current_group = []
                current_length = 0
            # Add the large article as its own group
            groups.append([article])
        else:
            if current_length + article_length > threshold:
                # Current group exceeds threshold, start a new group
                groups.append(current_group)
                current_group = [article]
                current_length = article_length
            else:
                # Add article to current group
                current_group.append(article)
                current_length += article_length

    # Add the last group if it's not empty
    if current_group:
        groups.append(current_group)

    return groups


class ArticleProcessor:
    def __init__(self):
        self.client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
        self.assistant = self.client.beta.assistants.retrieve(TO_JSON_ASSISTANT_ID)
        self.thread = self.client.beta.threads.create()
        with open(INSTRUCTIONS_FILE, "r") as f:
            self.instructions = f.read()
            # print("Instructions are:")
            # print(self.instructions)

    def submit_message(self, message, model):
        t0 = time.time()
        print(f"Using model: {model}")
        completion = self.client.chat.completions.create(
            model=model,
            response_format={"type": "json_object"},
            messages=[{"role": "system", "content": self.instructions}, {"role": "user", "content": message}],
        )
        body_text = completion.choices[0].message.content
        # print(body_text)
        response = get_json(body_text)
        t1 = time.time()
        avg_speed = round(len(body_text) / (t1 - t0), 2)
        print(f"Time elapsed: {round(t1-t0, 2)} seconds, average speed: {avg_speed} chars/second")
        return response

    def submit_message_wth_retries(self, message, retries=3, model=SIMPLE_GPT_MODEL):
        # Get count of occurences of "div class='article'" in message string
        article_count = message.count("div class='article'")
        # print(f"Expecing {article_count} articles")
        for i in range(retries):
            try:
                out = self.submit_message(message, model)
                if len(out) != article_count:
                    print(f"Error: response should contain {article_count} articles, but contains {len(out)}")
                    print(out)
                    i += 1
                    continue
                return out
            except Exception as e:
                print(f"Error: {e}")
                print(f"Retrying {i+1} out of {retries}")
        raise Exception(f"Failed to submit message after {retries} retries")

    def submit_large_article(self, article):
        new_message_size_threshold = 500 + len(article) / int(len(article) / MESSAGE_SIZE_THRESHOLD + 1)
        articles = split_article(article, new_message_size_threshold)
        if len(articles) > 1:
            print(f"Total chunks: {len(articles)}")
        i = 0
        out = []
        t0 = time.time()
        for a in articles:
            print(f"Submitting chunk {i+1} out of {len(articles)}, {len(a)} characters ...")
            response = self.submit_message_wth_retries(a, retries=MAX_RETRIES, model=COMPLEX_GPT_MODEL)
            out.append(response[0])
            i += 1
        t2 = time.time()
        print(f"Total time elapsed: {round(t2-t0, 2)} seconds")
        with open("out_in_processor.json", "w") as f:
            json.dump(out, f, indent=4)
        unified = unify_chunks(out)
        with open("out_in_processor_unified.json", "w") as f:
            json.dump(unified, f, indent=4)
        return [unified]

    def submit_article(self, article, model):
        print(f"Submitting an article of length: {len(article)}")
        if len(article) > MESSAGE_SIZE_THRESHOLD:
            print("This is a large article, need to split it")
            return self.submit_large_article(article)
        else:
            return self.submit_message_wth_retries(article, retries=MAX_RETRIES, model=model)

    def submit_multiple_articles(self, articles):
        print(f"Submitting {len(articles)} articles")
        groups = group_articles(articles, MESSAGE_SIZE_THRESHOLD)
        print(f"There will be {len(groups)} groups")
        for group in groups:
            print(f"Submitting a group of length: {len(group)}, total size: {sum([len(a) for a in group])}")
            inp = "\n\n".join(group)
            total_length = sum([len(a) for a in group])
            if len(group) >= 3 or total_length < MESSAGE_SIZE_THRESHOLD / 2:
                model = SIMPLE_GPT_MODEL
            else:
                model = COMPLEX_GPT_MODEL
            processed = self.submit_article(inp, model)
            # processed = self.submit_message_wth_retries(inp, retries=MAX_RETRIES, model=model)
            for article in processed:
                yield article
