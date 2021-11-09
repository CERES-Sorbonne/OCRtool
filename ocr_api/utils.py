import io
import logging
import os
import subprocess
import zipfile
from io import StringIO
from xml.sax.saxutils import escape
import xml.dom.minidom as dom

from typing import Literal, Tuple

from fastapi import HTTPException

MimeType = Literal["text/csv", "application/json", "text/plain", "text/xml",
                   "text/html", "application/x-zip-compressed"]

OutputType = Literal["csv", "json", "txt", "xml", "html", "zip"]
Output = Literal["txt", "xml", "html"]


def get_mimetype(output_type: OutputType) -> MimeType:
    if output_type == "csv":
        return "text/csv"
    elif output_type == "json":
        return "application/json"
    elif output_type == "txt":
        return "text/plain"
    elif output_type == "xml":
        return "text/xml"
    elif output_type == "html":
        return "text/html"
    elif output_type == "zip":
        return "application/x-zip-compressed"


def pipeline(directory: str, output_type: OutputType) -> Tuple[io.BytesIO, OutputType]:
    result_type: OutputType = "zip"
    ocr_output, flag = ["txt", "-t"] if output_type in ['txt', 'xml'] else ["html", '-h']
    s = io.BytesIO()
    zf = zipfile.ZipFile(s, "w")
    pdf_names = [f.split('.')[0] for f in os.listdir(directory)]
    proc = subprocess.Popen([os.getenv("OCR_SCRIPT"), '-p', flag, '-k', directory], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    for line in io.TextIOWrapper(proc.stdout, encoding="utf-8"):
        logging.getLogger('ocr_api').warning(line)
    return_code = proc.wait(300)
    if return_code != 0:
        raise HTTPException(status_code=500, detail="There was an error during document conversion")
    for pdf_name in pdf_names:
        res = "<document>" if output_type == "xml" else ""
        files = [f for f in os.listdir(directory) if f.startswith(pdf_name) and f.endswith(ocr_output)]
        for i, f in enumerate(files):
            with open(os.path.join(directory, f), 'r') as fb:
                if output_type == "xml":
                    res += f'<page id="{i + 1}">'
                    res += escape(fb.read())
                    res += "</page>"
                else:
                    res += fb.read()
        if output_type == "xml":
            res += "</document>"
            res = dom.parseString(res).toprettyxml()
        zf.writestr(f"{pdf_name}.{output_type}", res)
    zf.close()
    return s, result_type
