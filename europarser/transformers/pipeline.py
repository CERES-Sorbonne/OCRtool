import json
from typing import Literal, List, Any, Tuple

from europarser.models import FileToTransform, Output, Pivot, OutputType, MimeType, get_mimetype
from europarser.transformers.pivot import PivotTransformer


def pipeline(files: List[FileToTransform], output: Output = "pivot") -> Tuple[str, OutputType, MimeType]:
    pivots: List[Pivot] = []
    for file_to_process in files:
        transformed: List[Pivot] = PivotTransformer().transform(file_to_process)
        pivots = [*pivots, *transformed]
    if output == "cluster_tool":
        result = json.dumps({i: article.dict() for i, article in enumerate(pivots)}, ensure_ascii=False)
        result_type: OutputType = "json"
        result_mimetype = get_mimetype(result_type)
    else:
        result = json.dumps([pivot.dict() for pivot in pivots], ensure_ascii=False)
        result_type: OutputType = "json"
        result_mimetype = get_mimetype(result_type)
    return result, result_type, result_mimetype
