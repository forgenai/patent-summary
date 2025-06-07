from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class PatentRequest(BaseModel):
    patent_number: str

@app.post("/summarize")
def summarize(req: PatentRequest):
    summary = summarize_patent(req.patent_number)
    return {"summary": summary}
