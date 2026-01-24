from openai import OpenAI


class OpenAIAdapter:
    def __init__(self):
        self.client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
        self.default_model = "gpt-5-nano"

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


if __name__ == "__main__":
    import os

    from dotenv import load_dotenv

    load_dotenv()
    adapter = OpenAIAdapter()
    response = adapter.generate_response(
        system="", user="What is the capital of France?"
    )
    print(response)
