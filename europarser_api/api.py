import io
import os
from typing import Optional, List

from fastapi import FastAPI, File, UploadFile, Request, Form
from fastapi.responses import StreamingResponse, HTMLResponse
from fastapi.templating import Jinja2Templates

from europarser.models import FileToTransform, Output
from europarser.transformers.pipeline import pipeline

app = FastAPI()
templates = Jinja2Templates(directory=os.path.join(os.path.dirname(__file__), "templates"))


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse('main.html', {'request': request})


@app.post("/upload")
async def handle_files(files: List[UploadFile] = File(...), output: Optional[Output] = Form(...)):
    # parse all files
    to_process = [FileToTransform(name=f.filename, file=f.file.read().decode('utf-8')) for f in files]
    # process result
    result, result_type, result_mimetype = pipeline(to_process, output)
    # stream result as file
    response = StreamingResponse(io.StringIO(result), media_type=result_mimetype)
    response.headers["Content-Disposition"] = f"attachment; filename=result.{result_type}"
    return response