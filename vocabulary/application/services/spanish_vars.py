from typing import List


class SpanishPrompts:
    @staticmethod
    def sentences(*, word: str) -> str:
        return (
            f"""
        Generate 7 sentences in Spanish using the word "{word}".
        Each sentence should be simple and easy to understand for a beginner learner of Spanish.
        Each sentence should be no longer than 7 words and should include the word "{word}" in a natural way.
        Each sentence should be common used in everyday conversation.
        """
            + """
        return the sentences as a list of strings in format:
        {
            "sentences": [
                "sentence 1",
                "sentence 2",
                "sentence 3"
            ]
        }"""
        )

    @staticmethod
    def detect_word(*, sentences: List[str], word: str) -> str:
        return (
            f"""
        Given the following sentences in Spanish:
        {"\n".join(sentences)}
        Each sentence contains a word "{word}" in Spanish.
        Identify that word in each sentence and return a list of the forms of the word "{
                word
            }" used in each sentence.
        For example, if the word is "hablar" and the sentences are:
        "Yo hablo español."
        "Tú hablas inglés."
        "Él habla francés."
        The output should be: """
            + """
        {
            "forms": [
                "hablo",
                "hablas",
                "habla"
            ]
        }
        """
        )
