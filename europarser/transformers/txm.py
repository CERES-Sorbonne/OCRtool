import io
from typing import List

from europarser.models import Pivot
from europarser.transformers.transformer import Transformer


class TXMTransformer(Transformer):
    def __init__(self):
        super(TXMTransformer, self).__init__()

    def transform(self, pivot_list: List[Pivot]) -> str:
        with io.StringIO() as f:
            f.write("<corpus>")
            for pivot in pivot_list:
                f.write("<article>")
                f.write("<titre>")
                f.write(pivot.titre)
                f.write("</titre>")
                f.write("<journal>")
                f.write(pivot.journal)
                f.write("</journal>")
                f.write("<date>")
                f.write(pivot.date)
                f.write("</date>")
                f.write("<texte>")
                f.write(pivot.texte)
                f.write("</texte>")
                f.write("</article>")
            f.write("</corpus>")
            return f.getvalue()