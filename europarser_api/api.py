import os
import tempfile
from typing import Optional, List

from fastapi import FastAPI, UploadFile, Request, Form, HTTPException, File
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, Response
from fastapi.templating import Jinja2Templates

from europarser_api.utils import get_mimetype, pipeline, Output

root_dir = os.path.dirname(__file__)
app = FastAPI()

app.mount("/ocr/static", StaticFiles(directory=os.path.join(root_dir, "static")), name="static")
templates = Jinja2Templates(directory=os.path.join(root_dir, "templates"))


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse('main.html', {'request': request})


@app.post("/upload")
async def handle_files(files: List[UploadFile] = File(...), output: Optional[Output] = Form(...)):
    if len(files) == 1 and files[0].filename == "":
        raise HTTPException(status_code=400, detail="No File Provided")
    with tempfile.TemporaryDirectory() as directory:
        for file in files:
            path = os.path.join(directory, file.filename)
            with open(path, 'wb') as f:
                f.write(file.file.read())
        result, result_type = pipeline(directory, output)
        # parse all files
        # process result
        result_mimetype = get_mimetype(result_type)
        # stream result as file
        response = Response(result.getvalue(), media_type=result_mimetype)
        response.headers["Content-Disposition"] = f"attachment; filename=result.{result_type}"
        return response