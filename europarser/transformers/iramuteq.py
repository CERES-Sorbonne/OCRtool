import io
from typing import List

from europarser.models import Pivot
from europarser.transformers.transformer import Transformer


class IramuteqTransformer(Transformer):
    def __init__(self):
        super(IramuteqTransformer, self).__init__()

    def transform(self, pivot_list: List[Pivot]) -> str:
        keys = pivot_list[0].dict().keys()
        with io.StringIO() as f:
            head = f"**** {' '.join(['*' + k for k in keys])}"
            f.write('\n')
            f.write(head)
            for pivot in pivot_list:
                f.write('\n')
                values = " ".join(pivot.dict().values())
                f.write(values)
            return f.getvalue()
