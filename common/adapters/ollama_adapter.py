import ollama

from common.ports.llm_adapter import LLMAdapter


class OllamaAdapter(LLMAdapter):
    def generate_response(
        self,
        *,
        system: str,
        user: str,
    ) -> str:
        response = ollama.chat(
            model="gemma2:2b",
            messages=[
                {"role": "user", "content": system},
                {"role": "user", "content": user},
            ],
        )
        content = response["message"]["content"]

        return "\n".join([line for line in content.split("\n") if "`" not in line])


ollama_adapter = OllamaAdapter()

if __name__ == "__main__":
    response = ollama_adapter.generate_response(
        system="", user="What is the capital of France?"
    )
    print(response)
