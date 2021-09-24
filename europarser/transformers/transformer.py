import logging
from abc import ABC
from typing import List

from europarser.models import Error, Pivot


class Transformer(ABC):
    def __init__(self):
        self.type: str = type(self).__name__
        self.errors: List[Error] = []
        self._logger = logging.getLogger(self.type)

    def transform(self, pivot: List[Pivot]) -> str:
        pass

    def _log_error(self, error, article):
        self.errors.append(Error(message=str(error), article=article.text, transformer=self.type))