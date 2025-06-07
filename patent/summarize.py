import os
from dotenv import load_dotenv
from openai import OpenAI
from forgen.pipeline.builder import SerialPipelineBuilder
from forgen.llm_interface.openai.openai_interface import get_openai_chat_completions_response

load_dotenv()

# ─────────────────────────────────────────────────────────
# SCHEMAS

input_schema = {
    "custom_instruction": str,
    "full_text": str
}
output_schema = {
    "summary": str
}

# ─────────────────────────────────────────────────────────
# PHASE 1: Chunking Full Text into Manageable Parts

def chunk_full_text(input_data):
    full_text = input_data.get("full_text", "")
    custom_instruction = input_data.get("custom_instruction", "")
    max_words_per_chunk = 10000

    words = full_text.split()
    chunks = [
        " ".join(words[i:i+max_words_per_chunk])
        for i in range(0, len(words), max_words_per_chunk)
    ]

    return {
        "chunked_inputs": [
            {
                "custom_instruction": custom_instruction,
                "text_chunk": chunk
            }
            for chunk in chunks
        ]
    }

# ─────────────────────────────────────────────────────────
# PHASE 2: Generate a Technical Summary for Each Chunk

def summarize_chunks(input_data, openai_client=None):
    chunked_inputs = input_data["chunked_inputs"]
    all_summaries = []

    for chunk in chunked_inputs:
        prompt = (
            "You are a professional patent analyst. Write a technical summary of this patent chunk.\n"
            "Focus on:\n"
            "- The technical problem being addressed\n"
            "- The core inventive solution\n"
            "- Any unique mechanisms or techniques\n\n"
            "Write clearly and concisely for engineers. No fluff or marketing tone."
        )

        if chunk["custom_instruction"]:
            prompt = f"INSTRUCTION:\n{chunk['custom_instruction']}\n\n" + prompt

        user_content = chunk["text_chunk"]

        response = get_openai_chat_completions_response(
            message_history=[],
            system_content=prompt,
            user_content=user_content,
            username="",
            json_response=False,
            openai_client=openai_client
        )

        all_summaries.append(response.strip() if isinstance(response, str) else response["output"] if "output" in response else response)

    return {"partial_summaries": all_summaries}

# ─────────────────────────────────────────────────────────
# PHASE 3: Merge Summaries into One Coherent Output

def merge_summaries(input_data, openai_client=None):
    summaries = input_data.get("partial_summaries", [])
    if len(summaries) == 1:
        return {"summary": summaries[0]}
    prompt = (
        "Given the following individual summaries of a patent document, synthesize them into one clear, concise technical summary. "
        "Focus on identifying the central technical problem and the inventive solution. Keep the language objective and professional."
    )

    combined_input = "\n\n".join(summaries)

    response = get_openai_chat_completions_response(
        message_history=[],
        system_content=prompt,
        user_content=combined_input,
        username="",
        json_response=False,
        openai_client=openai_client
    )

    return {"summary": response.strip() if isinstance(response, str) else response["output"] if "output" in response else response}

# ─────────────────────────────────────────────────────────
# PIPELINE ASSEMBLY

def build_summary_pipeline(openai_client):
    builder = SerialPipelineBuilder("PatentTextSummarizer", openai_client=openai_client)
    builder.set_description("Pipeline to summarize full patent text into technical problem/solution summary.")
    builder.set_input_schema(input_schema)
    builder.set_global_output_schema(output_schema)

    builder.create_and_add_node(
        operative_fn=chunk_full_text,
        operative_output_schema={"chunked_inputs": list},
        is_generative_node=False
    )

    builder.create_and_add_node(
        operative_fn=summarize_chunks,
        operative_input_schema={"chunked_inputs": list},
        operative_output_schema={"partial_summaries": list},
        is_generative_node=True
    )

    builder.create_and_add_node(
        operative_fn=merge_summaries,
        operative_input_schema={"partial_summaries": list},
        operative_output_schema={"summary": str},
        is_generative_node=True
    )

    return builder.build()

# ─────────────────────────────────────────────────────────
# MAIN EXECUTION (test mode)

openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
summarizer_tool = build_summary_pipeline(openai_client)

def summarize_patent_text(full_text: str, custom_instruction: str = "") -> str:
    input_data = {
        "full_text": full_text,
        "custom_instruction": custom_instruction
    }
    result = summarizer_tool.execute(input_data)
    return result["summary"]

#
# if __name__ == "__main__":
#     with open("example_inputs/full_text_input.json", "r") as f:
#         test_input = json.load(f)
#     summary = summarize_patent_text(test_input["full_text"], test_input.get("custom_instruction", ""))
#     print("FINAL SUMMARY:\n")
#     print(summary)
