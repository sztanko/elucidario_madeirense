import os
import time
import json
from openai import OpenAI
from collections import defaultdict
import traceback
from datetime import datetime

from processor.splitter import split_article
from processor.constants import DEFAULT_INSTRUCTIONS_FILE, DEFAULT_SIMPLE_GPT_MODEL, DEFAULT_COMPLEX_GPT_MODEL, DEFAULT_MESSAGE_SIZE_THRESHOLD
from processor.output_utils import get_json, unify_chunks, group_articles


MAX_RETRIES = 4



class ArticleProcessor:
    def __init__(
        self,
        instructions_file=DEFAULT_INSTRUCTIONS_FILE,
        message_size_threshold=DEFAULT_MESSAGE_SIZE_THRESHOLD,
        simple_gpt_model=DEFAULT_SIMPLE_GPT_MODEL,
        complex_gpt_model=DEFAULT_COMPLEX_GPT_MODEL,
    ):
        if "OPENAI_API_KEY" not in os.environ:
            raise Exception("OPENAI_API_KEY not found in environment variables")
        self.client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
        self.thread = self.client.beta.threads.create()
        self.message_size_threshold = message_size_threshold
        self.simple_gpt_model = simple_gpt_model
        self.complex_gpt_model = complex_gpt_model
        with open(instructions_file, "r") as f:
            self.instructions = f.read()
            # print("Instructions are:")
            # print(self.instructions)

    def determine_model(self, message):
        if ".............." in message:
            return self.complex_gpt_model
        return self.simple_gpt_model

    def submit_message(self, message):
        t0 = time.time()
        t0_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        model = self.determine_model(message)
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
        for a in response:
            a["debug"] = {
                "model": model,
                "chunk_time": round(t1 - t0, 2),
                "ts": t0_str,
                "chars": len(body_text),
                "avg_speed": avg_speed,
            }
        print(f"Time elapsed: {round(t1-t0, 2)} seconds, average speed: {avg_speed} chars/second")
        return response

    def submit_message_wth_retries(self, message, retries=3):
        # Get count of occurences of "div class='article'" in message string
        article_count = message.count("div class='article'")
        # print(f"Expecing {article_count} articles")
        for i in range(retries):
            try:
                out = self.submit_message(message)
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
        new_message_size_threshold = 500 + len(article) / int(len(article) / self.message_size_threshold + 1)
        articles = split_article(article, new_message_size_threshold)
        if len(articles) > 1:
            print(f"Total chunks: {len(articles)}")
        i = 0
        out = []
        t0 = time.time()
        for a in articles:
            print(f"Submitting chunk {i+1} out of {len(articles)}, {len(a)} characters ...")
            response = self.submit_message_wth_retries(a, retries=MAX_RETRIES)
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

    def submit_article(self, article):
        print(f"Submitting an article of length: {len(article)}")
        if len(article) > self.message_size_threshold:
            print("This is a large article, need to split it")
            return self.submit_large_article(article)
        else:
            return self.submit_message_wth_retries(article, retries=MAX_RETRIES)

    def submit_multiple_articles(self, articles):
        print(f"Submitting {len(articles)} articles")
        groups = group_articles(articles, self.message_size_threshold)
        print(f"There will be {len(groups)} groups")
        c = 0
        with open(f"debug.txt", "w") as f:
            for group in groups:
                now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                print(f"Submitting a group of length: {len(group)}, total size: {sum([len(a) for a in group])}")
                f.write(
                    f"{now}:\tSubmitting a group of length: {len(group)}, total size: {sum([len(a) for a in group])}\n"
                )
                inp = "\n\n".join(group)
                try:
                    processed = self.submit_article(inp)
                    for article in processed:
                        yield article
                except Exception as e:
                    print(f"Error: {e}")
                    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    f.write(f"{now}\n")
                    f.write(f"Error: {e}\n")
                    # write out chunk output to a separate file
                    with open(f"chunk_{c}.txt", "w") as f2:
                        f2.write(inp)
                    # print stacktrace to file
                    traceback.print_exc(file=f)
                    f.write("\n\n")
                c += 1
