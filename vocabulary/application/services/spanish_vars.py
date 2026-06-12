class SpanishPrompts:
    @staticmethod
    def sentences(*, word: str):
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
