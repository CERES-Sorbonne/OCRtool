import io
import json
from typing import Optional, List

from fastapi import FastAPI, File, UploadFile
from fastapi.responses import StreamingResponse

from europarser.models import FileToTransform, Output
from europarser.transformers.pipeline import pipeline

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/upload")
async def handle_files(files: List[UploadFile] = File(...), output: Optional[Output] = "pivot"):
    # parse all files
    to_process = [FileToTransform(name=f.filename, file=f.file.read().decode('utf-8')) for f in files]
    # process result
    result, result_type, result_mimetype = pipeline(to_process, output)
    # stream result as file
    response = StreamingResponse(io.StringIO(result), media_type=result_mimetype)
    response.headers["Content-Disposition"] = f"attachment; filename=result.{result_type}"
    return response