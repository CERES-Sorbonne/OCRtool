from enum import Enum
from typing import Literal

from pydantic import BaseModel


class FileToTransform(BaseModel):
    name: str
    file: str


class Error(BaseModel):
    message: str
    article: str
    transformer: str


class Pivot(BaseModel):
    journal: str
    date: str
    titre: str
    texte: str


OutputType = Literal["csv", "json", "txt"]
Output = Literal["pivot", "txm", "iramuteq", "gephi", "cluster_tool"]
MimeType = Literal["text/csv", "application/json", "text/plain"]


def get_mimetype(output_type: OutputType) -> MimeType:
    if output_type == "csv":
        return "text/csv"
    elif output_type == "json":
        return "application/json"
    elif output_type == "txt":
        return "text/plain"
