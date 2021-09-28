import io
import os
from typing import Optional, List

from fastapi import FastAPI, File, UploadFile, Request, Form, HTTPException
from fastapi.responses import StreamingResponse, HTMLResponse
from fastapi.templating import Jinja2Templates

from europarser.models import FileToTransform, Output
from europarser.transformers.pipeline import pipeline
from europarser_api.utils import get_mimetype

app = FastAPI()
templates = Jinja2Templates(directory=os.path.join(os.path.dirname(__file__), "templates"))


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse('main.html', {'request': request})


@app.post("/upload")
async def handle_files(files: List[UploadFile], output: Optional[Output] = Form(...)):
    if len(files) == 1 and files[0].filename == "":
        raise HTTPException(status_code=400, detail="No File Provided")
    # parse all files
    to_process = [FileToTransform(name=f.filename, file=f.file.read().decode('utf-8')) for f in files]
    # process result
    result, result_type = pipeline(to_process, output)
    result_mimetype = get_mimetype(result_type)
    # stream result as file
    response = StreamingResponse(io.StringIO(result), media_type=result_mimetype)
    response.headers["Content-Disposition"] = f"attachment; filename=result.{result_type}"
    return response