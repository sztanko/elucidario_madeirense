from typing import List, Dict, Callable, Any
import logging
import os
from processor.llm.processor import Processor
from processor.llm.engines import AIEngine
import time
from datetime import datetime

Article = Dict

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(filename)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()],
)

MAX_RETRIES = 2


FIRST_TIMESTAMP = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
FIRST_TIMESTAMP_UNDERSCORE = datetime.now().strftime("%Y_%m_%d__%H_%M_%S")
BASE_TS = time.time()

SUBMIT_LOG = f"submit_log_{FIRST_TIMESTAMP_UNDERSCORE}.txt"


def split_article(article: Article, threshold: int, splitter: Callable[[Article, int], List[Article]]) -> List[Article]:
    pass


class Submitter:
    def __init__(self, processor: Processor, threshold: int, fail_dir: str):
        self.processor = processor
        self.threshold = threshold
        self.fail_dir = fail_dir

    def group_articles(self, articles: List[str]) -> List[List[str]]:
        groups: List[List[str]] = []

        for article in articles:
            article_length: int = len(article)
            if article_length > self.threshold:
                groups.append([article])
            else:
                # Find a suitable group for the article
                added_to_group = False
                for group in groups:
                    group_length = sum(len(a) for a in group)
                    if group_length + article_length <= self.threshold:
                        group.append(article)
                        added_to_group = True
                        break
                if not added_to_group:
                    groups.append([article])

        return groups

    def submit_with_retry(self, group_id, message: str, engine: AIEngine, parser, num_items: int) -> Any:
        try_count = 0
        output = ""
        tb = time.time()
        error = None
        while try_count < MAX_RETRIES:
            try:
                t0 = time.time()
                output = engine.submit_message(message)
                t1 = time.time()
                avg_speed = round(len(message) / (t1 - t0), 2)
                result = parser(output)
                logging.info(
                    f"Submission successfull. Time elapsed: {round(t1-t0, 2)} seconds, average speed: {avg_speed} chars/second"
                )
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                with open(SUBMIT_LOG, "a") as f:
                    f.write(
                        "\t".join(
                            [
                                FIRST_TIMESTAMP,
                                str(t1 - BASE_TS),
                                str(group_id),
                                timestamp,
                                str(num_items),
                                str(round(t1 - tb, 2)),
                                str(avg_speed),
                                str(try_count),
                                str(engine.__class__.__name__),
                                "success",
                                "",
                            ]
                        )
                        + "\n"
                    )
                return result
            except Exception as e:
                logging.info(f"Received this output: \n {output}")
                logging.warning(f"Error: {e}")
                logging.exception(e)

                try_count += 1
                if try_count == 3:
                    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    logging.error(f"Group {group_id} Failed after {try_count} attempts on {timestamp}")
                    logging.exception(e)
                    logging.info(f"Saving message to {self.fail_dir}")
                    if not os.path.exists(self.fail_dir):
                        os.makedirs(self.fail_dir)
                    file_name = f"{self.fail_dir}/{group_id}_{FIRST_TIMESTAMP}_{time.time()}.txt"
                    with open(file_name, "w") as f:
                        f.write(message)
                    t1 = time.time()
                    with open(SUBMIT_LOG, "a") as f:
                        f.write(
                            "\t".join(
                                [
                                    FIRST_TIMESTAMP,
                                    str(t1 - BASE_TS),
                                    str(group_id),
                                    timestamp,
                                    str(num_items),
                                    str(round(t1 - tb, 2)),
                                    "0",
                                    str(try_count),
                                    str(engine.__class__.__name__),
                                    "fail",
                                    str(e),
                                ]
                            )
                            + "\n"
                        )
                    raise
                else:
                    logging.warning(f"Retrying... Attempt {try_count+1}/{MAX_RETRIES}")
                    continue

    def submit_articles(self, articles: List[str]):
        groups = self.group_articles(articles)
        logging.info(f"Submitting {len(groups)} groups out of {len(articles)} articles")
        group_no = 0
        for group in groups:
            message = self.processor.to_message(group)
            logging.info(
                f"Submitting group {group_no+1} out of {len(groups)}, size of group: {len(group)} article(s) of {len(message)} characters"
            )
            try:
                if len(group) == 1:
                    article = group[0]
                    article_size = len(article)
                    if article_size > self.threshold:
                        # Split article
                        logging.info(f"Splitting article of size {article_size} into chunks")
                        parts = self.processor.split_articles(article, self.threshold)
                        chunks = []
                        chunk_no = 0
                        for part in parts:
                            logging.info(f"Submitting chunk {chunk_no+1} out of {len(parts)}")
                            partial_message = self.processor.to_message([part])
                            chunk_result = self.submit_with_retry(
                                group_no,
                                partial_message,
                                self.processor.get_partial_article_engine(),
                                self.processor.parse_chunk_result,
                                len(group),
                            )
                            chunks.append(chunk_result)
                            chunk_no += 1
                        result = self.processor.merge_results(chunks)
                    else:
                        result = self.submit_with_retry(
                            group_no,
                            message,
                            self.processor.get_single_article_engine(),
                            self.processor.parse_result,
                            len(group),
                        )
                    yield result
                else:
                    logging.info(f"Submitting {len(group)} articles at once, total size: {len(message)}")
                    results = self.submit_with_retry(
                        group_no,
                        message,
                        self.processor.get_multiple_articles_engine(),
                        self.processor.parse_multiple_result,
                        len(group),
                    )
                    for result in results:
                        yield result
            except Exception as e:
                logging.error(f"Error: {e}")
                logging.exception(e)
            group_no += 1
        logging.info("Done submitting articles")
