import os
from dotenv import load_dotenv
from openai import OpenAI
from forgen.pipeline.builder import SerialPipelineBuilder
from uspto_data.uspto_client import USPTOClient
from uspto_data.query.patent import USPatent
from uspto_data.query.publication import USPublication

load_dotenv()
uspto_client = USPTOClient(api_key=os.getenv("USPTO_API_KEY"))

# ─────────────────────────────────────────────────────────
# SCHEMA

input_schema = {
    "document_number": str  # Can be a US patent or publication number
}
output_schema = {
    "full_text": str,
    "resolved_type": str
}

# ─────────────────────────────────────────────────────────
# HELPER

def resolve_document_type(document_number: str) -> str:
    """
    Heuristic to decide whether it's a patent or a publication.
    """
    clean = document_number.replace(",", "").replace("/", "").strip()
    if len(clean) <= 8:
        return "patent"
    return "publication"

# ─────────────────────────────────────────────────────────
# NODE LOGIC

def fetch_uspto_text(input_data, openai_client=None):
    doc_number = input_data["document_number"]
    doc_type = resolve_document_type(doc_number)

    if doc_type == "patent":
        doc = USPatent(doc_number, uspto_client=uspto_client, auto_load=True)
    else:
        doc = USPublication(doc_number, uspto_client=uspto_client, auto_load=True)

    content = doc.get_published_content()

    try:
        text = content.get_description_text()
    except Exception:
        text = content.xml if hasattr(content, "xml") else str(content)

    return {
        "full_text": text or "",
        "resolved_type": doc_type
    }

# ─────────────────────────────────────────────────────────
# PIPELINE WRAPPER

def build_text_fetch_pipeline(openai_client):
    builder = SerialPipelineBuilder("PatentTextFetcher", openai_client=openai_client)
    builder.set_description("Resolves a patent/publication number and fetches the full description text.")
    builder.set_input_schema(input_schema)
    builder.set_global_output_schema(output_schema)

    builder.create_and_add_node(
        operative_fn=fetch_uspto_text,
        operative_output_schema={"full_text": str, "resolved_type": str},
        is_generative_node=False
    )

    return builder.build()

# ─────────────────────────────────────────────────────────
# OPTIONAL LOCAL TEST

openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
text_pipeline = build_text_fetch_pipeline(openai_client)

if __name__ == "__main__":
    test_input = {"document_number": "10001001"}
    result = text_pipeline.execute(test_input)
    print("Resolved Type:", result["resolved_type"])
    print("Full Text Snippet:\n", result["full_text"][:1000])
