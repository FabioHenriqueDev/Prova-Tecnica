from openai import OpenAI
from dotenv import load_dotenv
import os
from src.prompt.prompt import prompt_agent
from src.schemas.schema import CompanyExtraction
import time
import json

load_dotenv()

def extract_agent(page_markdown: str):
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    response = client.responses.parse(
        model="gpt-4o-mini",
        input = [
            {
                "role": "system", 
                "content": prompt_agent
            },
            {
                "role": "user", 
                "content": f"TEXTO DO SITE:\n{page_markdown}" 
            }
        ],
        text_format = CompanyExtraction 
    )

    time.sleep(5)

    parse_data_pydantic = response.output_parsed

    if parse_data_pydantic:
        with open("dados.json", 'w', encoding="utf-8") as a:
            json.dump(response.model_dump(), a, ensure_ascii=False, indent=4)

    return parse_data_pydantic