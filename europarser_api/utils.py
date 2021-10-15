import io
import os
import subprocess
import zipfile
from io import StringIO
from xml.sax.saxutils import escape
import xml.dom.minidom as dom

from typing import Literal, Tuple

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
    ocr_output = "txt" if output_type in ['txt', 'xml'] else "html"
    s = io.BytesIO()
    zf = zipfile.ZipFile(s, "w")
    pdf_names = [f.split('.')[0] for f in os.listdir(directory)]
    subprocess.check_call([r"/home/tyra/Documents/CERES/ocr/test.sh", directory])
    for pdf_name in pdf_names:
        res = "<document>" if output_type == "xml" else ""
        path = os.path.join(directory, pdf_name)
        files = [f for f in os.listdir(path) if f.endswith(ocr_output)]
        for i, f in enumerate(files):
            with open(os.path.join(path, f), 'r') as fb:
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