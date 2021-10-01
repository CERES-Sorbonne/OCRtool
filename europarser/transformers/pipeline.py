import json
from typing import List, Tuple

from europarser.models import FileToTransform, Output, Pivot, OutputType
from europarser.transformers.iramuteq import IramuteqTransformer
from europarser.transformers.pivot import PivotTransformer
from europarser.transformers.txm import TXMTransformer


def pipeline(files: List[FileToTransform], output: Output = "pivot") -> Tuple[str, OutputType]:
    pivots: List[Pivot] = []
    for file_to_process in files:
        transformed: List[Pivot] = PivotTransformer().transform(file_to_process)
        pivots = [*pivots, *transformed]
    if output == "cluster_tool":
        result = json.dumps({i: article.dict() for i, article in enumerate(pivots)}, ensure_ascii=False)
        result_type: OutputType = "json"
    elif output == "iramuteq":
        result = IramuteqTransformer().transform(pivots)
        result_type = "txt"
    elif output == "txm":
        result = TXMTransformer().transform(pivots)
        result_type = "xml"
    else:
        result = json.dumps([pivot.dict() for pivot in pivots], ensure_ascii=False)
        result_type: OutputType = "json"
    return result, result_type
