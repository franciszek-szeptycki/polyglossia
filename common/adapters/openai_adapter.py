import json
import os
from logging import getLogger

from dotenv import load_dotenv
from openai import OpenAI

from common.ports.llm_adapter import LLMAdapter

load_dotenv()
logger = getLogger(__name__)


class OpenAIAdapter(LLMAdapter):
    def __init__(self):
        self.client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
        # self.default_model = "gpt-4o-mini"
        self.default_model = "gpt-4o"

    def generate_response(
        self,
        *,
        system: str,
        user: str,
    ) -> str:
        response = self.client.chat.completions.create(
            model=self.default_model,
            messages=[
                # {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
            response_format={"type": "json_object"},
        )
        return response.choices[0].message.content

    def prompt_json(
        self,
        *,
        user: str,
    ) -> dict:
        try:
            logger.info(f"Prompting LLM with user message: {user[:20]}...")
            response = self.client.chat.completions.create(
                model=self.default_model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a helpful assistant designed to output JSON.",
                    },
                    {"role": "user", "content": user},
                ],
                response_format={"type": "json_object"},
            )
            return json.loads(response.choices[0].message.content)
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON response: {e}")
            raise e
        except Exception as e:
            logger.error(f"An error occurred while generating response: {e}")
            raise e


if __name__ == "__main__":
    openai_adapter = OpenAIAdapter()
    response = openai_adapter.generate_response(
        system="", user="What is the capital of France?"
    )
