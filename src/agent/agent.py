from openai import OpenAI
from dotenv import load_dotenv
import os
from src.prompt.prompt import prompt_agent
from src.schemas.schema import CompanyExtraction

load_dotenv()

def extract_agent(page_markdown: str, url: str):
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
                "content": f"URL: {url}\n\nTEXTO DO SITE:\n{page_markdown}" 
            }
        ],
        text_format = CompanyExtraction 
    )

    return response.output_parsed