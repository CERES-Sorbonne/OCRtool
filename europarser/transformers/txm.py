from typing import List

from europarser.models import FileToTransform, Pivot
from europarser.transformers.transformer import Transformer


class TXMTransformer(Transformer):
    def __init__(self):
        super(TXMTransformer, self).__init__()

    def transform(self, pivot_list: List[Pivot]) -> str:
        pass