from typing import List, Dict
import logging
import json
from collections import defaultdict

from processor.llm.processor import Processor
from processor.utils.splitter import split_markdown
from processor.utils.instructions import load_instructions, make_output_schema_instructions
from models.article import Article
from models.translation import Translation
from models import create_list_model
from processor.llm.engines import OpenAIEngine, AIEngine, ClaudeEngine, GPT4Engine


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(filename)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()],
)


LANGUAGES = {
    "en": "English",
    "fr": "French",
    "de": "German",
    "uk": "Ukrainian",
    "ru": "Russian",
    "it": "Italian",
}

ENGINES = {
    "en": GPT4Engine,
    "fr": ClaudeEngine,
    "de": ClaudeEngine,
    "uk": ClaudeEngine,
    "ru": ClaudeEngine,
    "it": ClaudeEngine,
}


class TranslationProcessor(Processor):
    def __init__(self, lang: str, engine_str: str = None):
        super().__init__(engine_str=engine_str)
        logging.info(f"Initializing translation processor for {LANGUAGES[lang]}")
        self.output_schema = make_output_schema_instructions(Translation)
        self.output_schema_list = make_output_schema_instructions(Translation, as_list=True)
        if self.engine:
            engine = self.engine
        else:
            engine = ENGINES.get(lang)
        self.simple_article_engine = engine(
            load_instructions(
                "instructions/translate/translate_full.txt", output_schema=self.output_schema, lang=LANGUAGES[lang]
            )
        )
        self.multiple_articles_engine = engine(
            load_instructions(
                "instructions/translate/translate_full.txt", output_schema=self.output_schema_list, lang=LANGUAGES[lang]
            )
        )
        self.partial_article_engine = engine(
            load_instructions(
                "instructions/translate/translate_full.txt", output_schema=self.output_schema, lang=LANGUAGES[lang]
            )
        )

    def get_single_article_engine(self) -> AIEngine:
        return self.simple_article_engine

    def get_multiple_articles_engine(self) -> AIEngine:
        return self.multiple_articles_engine

    def get_partial_article_engine(self) -> AIEngine:
        return self.partial_article_engine

    def article_to_translation(self, article: Article) -> Translation:
        return Translation(**json.loads(article)).__dict__

    def to_message(self, articles: List[str]) -> str:
        if len(articles) == 1:
            return json.dumps(self.article_to_translation(articles[0]), ensure_ascii=False, indent=2)
        a = {"a": [self.article_to_translation(article) for article in articles]}
        return json.dumps(a, ensure_ascii=False, indent=2)

    def split_articles(self, message: str, threshold: int) -> List[str]:
        article = Article(**json.loads(message))
        splits = split_markdown(article.body, threshold)
        logging.info(f"Splitting article {article.id}({article.title}) into {len(splits)} chunks")
        previous_chunk = None
        out = []
        # First chunk is just metadata. It can be quite long in case of long articles.
        metadata_chunk = {
            "id": article.id,
            "title": article.title,
            "years": article.years,
            "people": article.people,
            "locations": article.locations,
            "body": "",
        }
        out.append(json.dumps(metadata_chunk, ensure_ascii=False, indent=2))
        for chunk in splits:
            chunk_dict = {"id": article.id, "title": article.title, "body": chunk}
            if previous_chunk:
                chunk_dict["preceeding_text"] = previous_chunk
            t = Translation(**chunk_dict)
            out.append(json.dumps(t.__dict__, ensure_ascii=False, indent=2))
            previous_chunk = " ".join(chunk.split()[-50:])
        return out

    def parse_result(self, result: str) -> Dict:
        res = json.loads(result)
        logging.info("Result is")
        logging.info(res)
        article = Translation(**res)
        return article.__dict__

    def parse_chunk_result(self, result: str) -> Dict:
        # In case of articles, it is same as parse_result
        return self.parse_result(result)

    def parse_multiple_result(self, result: str) -> List[Dict]:
        res = json.loads(result)
        results = []
        for a in res["a"]:
            try:
                article = Translation(**a)
                results.append(article.__dict__)
            except Exception as e:
                # This is not ideal, because we won't be retrying anything, but it's better than nothing
                logging.error(e)
                logging.error(a)
        return results

    def merge_results(self, results: List[Dict]) -> Dict:
        chunks = [Translation(**res) for res in results]
        merged_article = Translation(
            title=chunks[0].title,
            id=chunks[0].id,
            body="\n\n".join([chunk.body for chunk in chunks[1:]]),
            years=chunks[0].years,
            locations=chunks[0].locations,
            people=chunks[0].people,
        )
        return merged_article.__dict__
