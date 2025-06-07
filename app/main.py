from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from patent.tools import fetch_and_summarize_patent

app = FastAPI()

class SummarizeRequest(BaseModel):
    document_number: str
    custom_instruction: str = ""

@app.post("/summarize")
def summarize_patent(req: SummarizeRequest):
    try:
        summary = fetch_and_summarize_patent(req.document_number, req.custom_instruction)
        return {"summary": summary}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
