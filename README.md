# OCRtool
Simple tool to convert PDF files into text

## Running

Clone the repository locally
You need to set the OCR_SCRIPT environnment variable to the path pointing to the OCR script: see https://github.com/Tyrannas/IMG2TXT (this repository is a fork with some custom modifications, ideally this repository should be used when the PRs of the forked will be merged : https://github.com/jbtanguy/IMG2TXT).
For instance on linux:
```bash
export OCR_SCRIPT=/path/to/IMG2TXT/img2txt.sh
```

Then you just need to install the requirements with:
```bash
pip install -r requirements.txt
```

And run the API:
```bash
uvicorn ocr_api.api:app --reload
```
