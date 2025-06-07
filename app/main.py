import os

from fastapi import FastAPI, Request, HTTPException
import boto3
import urllib.parse
from pydantic import BaseModel
from patent.tools import fetch_and_summarize_patent

app = FastAPI()

class SummarizeRequest(BaseModel):
    document_number: str
    custom_instruction: str = ""

@app.post("/summarize")
def summarize_patent(req: SummarizeRequest):
    # , request: Request):
    # rapidapi_key = request.headers.get("X-RapidAPI-Proxy-Secret")
    # if rapidapi_key != os.environ.get("RAPIDAPI_KEY"):
    #     raise HTTPException(status_code=403, detail="Forbidden")
    try:
        summary = fetch_and_summarize_patent(req.document_number, req.custom_instruction)
        return {"summary": summary}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/register")
async def register_user(request: Request):
    # Parse the form data from the request body
    body = await request.body()
    form_fields = urllib.parse.parse_qs(body.decode())
    token = form_fields.get("x-amzn-marketplace-token", [None])[0]

    if not token:
        raise HTTPException(status_code=400, detail="Missing x-amzn-marketplace-token")

    try:
        # Create a Marketplace Metering client
        client = boto3.client('meteringmarketplace', region_name='us-east-1')

        # Call ResolveCustomer API
        response = client.resolve_customer(RegistrationToken=token)

        # Extract customer information
        customer_identifier = response['CustomerIdentifier']
        product_code = response['ProductCode']
        customer_aws_account_id = response['CustomerAWSAccountId']

        # TODO: Store customer information and provision access as needed

        return {
            "message": "User successfully registered",
            "customer_identifier": customer_identifier,
            "product_code": product_code,
            "customer_aws_account_id": customer_aws_account_id
        }

    except client.exceptions.InvalidTokenException:
        raise HTTPException(status_code=400, detail="Invalid token")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))