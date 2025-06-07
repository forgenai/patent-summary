from patent.fetch import text_pipeline as fetch_pipeline
from patent.summarize import summarizer_tool as summary_pipeline


def fetch_and_summarize_patent(document_number: str, custom_instruction: str = "") -> str:
    # Step 1: Fetch full text using the fetch pipeline
    fetch_input = {"document_number": document_number}
    fetch_result = fetch_pipeline.execute(fetch_input)

    full_text = fetch_result.get("full_text", "")
    if not full_text:
        raise ValueError("Failed to retrieve full text for the document.")

    # Step 2: Summarize full text using the summarizer
    summary_input = {
        "full_text": full_text,
        "custom_instruction": custom_instruction
    }
    summary_result = summary_pipeline.execute(summary_input)

    return summary_result["summary"]