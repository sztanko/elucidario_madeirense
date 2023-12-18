from typing import Any, Dict, List
from abc import ABC, abstractmethod

from processor.llm.engines import AIEngine


class Processor(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def get_single_article_engine(self) -> AIEngine:
        return None

    @abstractmethod
    def get_multiple_articles_engine(self) -> AIEngine:
        return AIEngine

    @abstractmethod
    def get_partial_article_engine(self) -> AIEngine:
        return None

    @abstractmethod
    def to_message(self, article: List[str]) -> str:
        return str

    @abstractmethod
    def split_articles(self, message: str, threshold: int) -> List[str]:
        return [message]

    @abstractmethod
    def parse_result(self, result: str) -> Dict:
        return {}

    @abstractmethod
    def parse_chunk_result(self, result: str) -> Dict:
        return {}

    @abstractmethod
    def parse_multiple_result(self, result: str) -> List[Dict]:
        return {}

    @abstractmethod
    def merge_results(self, results: List[str]) -> Dict:
        return {}
