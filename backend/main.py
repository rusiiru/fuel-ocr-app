from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from ocr_utils import extract_numbers_from_bytes, calc_fuel

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"],
                   allow_methods=["*"], allow_headers=["*"])

@app.post("/analyze/")
async def analyze(file: UploadFile = File(...)):
    data = await file.read()
    nums = extract_numbers_from_bytes(data)
    if not all(k in nums for k in ("left", "ctr", "right", "pre")):
        return {"error": "Missing values", "found": nums}
    return {**calc_fuel(nums["pre"], nums["left"], nums["ctr"], nums["right"]), "values": nums}
