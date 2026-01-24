from django.conf import settings
from openai import OpenAI


class OpenAIAdapter:
    def __init__(self, *, api_key: str):
        self.client = OpenAI(api_key=api_key)
        self.default_model = "gpt-5-nano"

    def generate_response(
        self,
        *,
        prompt: str,
        system_instructions: str,
    ):
        try:
            response = self.client.chat.completions.create(
                model=self.default_model,
                messages=[
                    {"role": "system", "content": system_instructions},
                    {"role": "user", "content": prompt},
                ],
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error: {str(e)}"


if __name__ == "__main__":
    import os

    from dotenv import load_dotenv

    load_dotenv()
    adapter = OpenAIAdapter(api_key=os.environ["OPENAI_API_KEY"])
    response = adapter.generate_response("What is the capital of France?")
    print(response)
