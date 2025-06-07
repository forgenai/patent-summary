import requests

def test_summarize_endpoint():
    url = "http://localhost:8000/summarize"
    payload = {
        "document_number": "9878232",
        "custom_instruction": "Summarize this simply."
    }
    headers = {
        "Content-Type": "application/json"
    }

    response = requests.post(url, json=payload, headers=headers)

    print("Status Code:", response.status_code)
    try:
        print("Response JSON:", response.json())
    except Exception:
        print("Response Text:", response.text)

# test_direct_call.py

from app.main import summarize_patent, SummarizeRequest

def test_direct_function_call():
    req = SummarizeRequest(
        document_number="9878232",
        custom_instruction="Summarize this simply."
    )
    result = summarize_patent(req)
    print("Summary:", result)

# Run it
if __name__ == "__main__":
    test_direct_function_call()
