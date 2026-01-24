import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()


class OpenAIAdapter:
    def __init__(self):
        self.client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
        self.default_model = "gpt-4o-mini"

    def generate_response(
        self,
        *,
        system: str,
        user: str,
    ):
        try:
            response = self.client.chat.completions.create(
                model=self.default_model,
                messages=[
                    {"role": "system", "content": system},
                    {"role": "user", "content": user},
                ],
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error: {str(e)}"


openai_adapter = OpenAIAdapter()

if __name__ == "__main__":
    response = openai_adapter.generate_response(
        system="", user="What is the capital of France?"
    )
    print(response)
